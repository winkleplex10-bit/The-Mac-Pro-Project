# MacPro6,2 — AM5 (Ryzen 7000/9000) vendor-BIOS + OpenCore firmware spec
Date: 2026-10-23. Status: draft v0.1. Public sources only. No NDA or leaked data was used, no vendor was contacted, and nothing was pushed or bought. Unknowns are marked **GAP**. Inputs: `am5-firmware-opencore-research.md`, `firmware-path-evaluation.md`.

Platform decision (Aidan, 2026-10-23): AM5 Ryzen 7000/9000 + licensed AMI Aptio V or InsydeH2O UEFI (AGESA), with OpenCore preloaded on a soldered NVMe (PCIe x1) boot drive. Goal: macOS, Windows and Linux boot with no user setup beyond our drivers (Navi23 GPU board, I/O board, SSD module).

Key sources:
- Dortania AMD Zen config + "AMD BIOS Settings": https://dortania.github.io/OpenCore-Install-Guide/AMD/zen.html
- AMD_Vanilla patches: https://github.com/AMD-OSX/AMD_Vanilla
- OpenCore Configuration.pdf: https://github.com/acidanthera/OpenCorePkg/blob/master/Docs/Configuration.pdf
- Dortania GPU Buyers Guide (Navi 23): https://dortania.github.io/GPU-Buyers-Guide/modern-gpus/amd-gpu.html
- AMD PSP integration (coreboot docs, public): https://doc.coreboot.org/soc/amd/psp_integration.html
- LVFS vendor onboarding: https://www.fwupd.org/lvfs/newaccount ; LVFS security/capsule DMI matching: https://lvfs.readthedocs.io/en/latest/security.html
- AMD capsule-on-disk note: https://review.coreboot.org/c/coreboot/+/93456/7

---

## 1. Requirements for the BIOS vendor (AMI / Insyde)

### 1.1 Factory default settings (shipped defaults, not "user must set")
Source for the macOS-relevant list: Dortania "AMD BIOS Settings" (zen.html, bottom section).

| # | Setting | Required default | Why / source |
|---|---|---|---|
| D1 | CSM | **Off** (UEFI only; CSM module ideally not built in) | Dortania: CSM "must be off", causes `gIO` GPU stalls. Also needed for Secure Boot and Windows 11. |
| D2 | Above 4G Decoding | **On** | Dortania: "must be on" (else `npci=0x3000`). Required for ReBAR. |
| D3 | Resizable BAR | **On** | Performance in Windows/Linux. In OpenCore set `Booter > Quirks > ResizeAppleGpuBars = 0` so macOS sees a size it accepts (Dortania zen.html). |
| D4 | CFG Lock / MSR lock | **N/A on AMD.** Dortania: `AppleCpuPmCfgLock`/`AppleXcpmCfgLock` "AMD users can ignore". No MSR 0xE2 equivalent is required. Ask vendor to not lock any MSR that AMDRyzenCPUPowerManagement writes (P-state MSRs). **GAP:** exact MSR list the kext writes; check its source before the RFQ. |
| D5 | Fast Boot | Off (or "minimal" that still enumerates all PCIe/NVMe) | Dortania lists Fast Boot as disable. |
| D6 | IOMMU | Default **Off** for macOS per Dortania; but Windows VBS/Kernel DMA Protection and Linux VFIO want it on. **Decision** (see §6). OpenCore can't hide IOMMU from macOS on AMD the way it can on Intel (`DisableIoMapper` is Intel VT-d only — Dortania). **GAP:** test whether current macOS boots on AM5 with IOMMU on. |
| D7 | XHCI hand-off | On | Dortania. |
| D8 | SATA mode | AHCI (no RAID) | Dortania. |
| D9 | Serial/parallel port | Off/absent | Dortania. |
| D10 | OS type | "Windows UEFI" | Dortania. |
| D11 | Secure Boot | **Enabled in User Mode with our keys**: our PK, our KEK + Microsoft KEK 2023 (and 2011 while still needed), db = our signing cert + Microsoft Windows PCA 2011/2023 + Microsoft UEFI CA 2011/2023. Keys provisioned at factory; Setup must allow reset-to-factory-keys and clear-to-Setup-Mode. Note Dortania's generic advice is "Secure Boot off" — we instead sign OpenCore + drivers (see `firmware-path-evaluation.md` §2). |
| D12 | Boot order | Pinned: `Boot0000` = onboard NVMe ESP-A `\EFI\OC\OpenCore.efi` (or `\EFI\BOOT\BOOTx64.efi`), `Boot0001` = ESP-B. Firmware must (a) not delete/reorder entries when other disks appear, (b) re-create these entries if NVRAM is reset, by device path of the soldered NVMe, (c) offer a hotkey for the one-time boot menu. OpenCore `RequestBootVarRouting=YES` keeps macOS Startup Disk from rewriting `BootOrder` (Dortania). |
| D13 | Fan/thermal, power-loss restore, RTC wake | Vendor default; must work from all OSes via ACPI. |
| D14 | PCIe link | GPU slot Gen4 x16 (Navi23 is Gen4 x8 electrically on retail RX 6600 cards — **GAP:** confirm our Navi23 board's lane count); NVMe boot drive Gen4 x1; SSD module Gen5/Gen4 x4. |

### 1.2 NVRAM
- Native, persistent UEFI variable store with ≥128 KB free authenticated space and garbage collection (macOS writes many vars; Dortania `WriteFlash=YES`). Must survive OS writes from macOS (via `OpenRuntime.efi`), Windows and Linux.
- Must not need `OpenVariableRuntimeDxe` (emulated NVRAM). Acceptance test: `nvram` set/read across reboots in macOS; `efivar` in Linux; Startup Disk works.
- MAT (`EFI_MEMORY_ATTRIBUTES_TABLE`) and a current EDK2 base, so `RebuildAppleMemoryMap` + `SyncRuntimePermissions` work (Dortania Booter quirks section explains failures on old EDK2 bases).
- **GAP:** whether `SetupVirtualMap` must be off on AM5 AGESA builds (Dortania notes B550/A520/TRx40 need it off). Test on first sample.

### 1.3 GOP for the Navi23 GPU board
- Our Navi23 board ships its own UEFI GOP in its option ROM (AMD supplies GOP for Radeon partners). Firmware must load signed PCIe option ROMs with Secure Boot on (signed by Microsoft UEFI CA or with our db cert).
- Optional fallback: vendor embeds the Navi23 GOP in the BIOS ROM. **GAP:** redistribution terms of AMD's GOP driver; ask the IBV.
- Require GOP output at pre-boot on the primary DP port, native panel resolution, so OpenCore picker + FileVault work.
- macOS: Navi 23 (RX 6600/6600 XT `73FF`, W6600 `73E3`) is natively supported since 12.1; needs Lilu + WhateverGreen and usually `agdpmod=pikera` (Dortania GPU Buyers Guide). **Pick a device ID macOS knows natively** (`73FF` or `73E3`) — this is a GPU-board decision with large impact.
- If Ryzen 9000/7000 iGPU is present, firmware default should be "dGPU primary"; macOS cannot use the Raphael/Granite Ridge iGPU (no Apple driver; RDNA2 iGPU support exists only via third-party NootedRed for APUs — not relevant to us). Option: disable iGPU by default to save BAR space. **Decision.**

### 1.4 SMBIOS fields
- Type 0/1/2/3/17 filled correctly by the BIOS (vendor, product "MacPro6,2"-branded name of our choice, our board version, BIOS version/date, memory SPD data).
- Type 1 UUID and Type 1/2 serials **unique per unit**, written at end-of-line into a protected SPI region that BIOS updates do not erase (like Dasharo's ROMHOLE, see firmware-path-evaluation §2).
- An OEM SMBIOS type (e.g., Type 11 OEM strings or a vendor type ≥128) carrying the per-unit Mac-format serial/MLB/ROM for OpenCore to read. **GAP:** OpenCore reads Apple identity from `PlatformInfo` (config/NVRAM), not from arbitrary OEM SMBIOS; we'd need either per-unit config injection or a small OC driver/tool. **Legal GAP** on generating Apple-format serials at all.
- DMI vendor string must be stable and ours (LVFS matches capsule updates by DMI, see §1.5).

### 1.5 Firmware update path
- UEFI capsule updates (FMP, ESRT published) signed with **our** key (vendor's capsule signing tool must accept our key).
- **Capsule-on-disk** support: on AMD, in-memory capsule handoff does not survive reset because the PSP invalidates it (coreboot change 93456, public). Ask AMI/Insyde to confirm their AMD capsule path.
- fwupd/LVFS: we open an LVFS vendor account (free; needs legal name, domain, PSIRT URL, redistribution permission letter — which requires the IBV and AMD to allow redistribution of the binary). LVFS matches UEFI capsules by DMI. **GAP:** whether AMI/Insyde/AMD licence terms permit public redistribution on LVFS; many OEMs (Lenovo, Dell, HP) do ship AMD capsules there, so precedent exists.
- Windows: same capsule as a Windows Update firmware driver package (CHID/ESRT based).
- macOS: no native path; our updater app stages the capsule to the ESP `\EFI\UpdateCapsule\` and sets `OsIndications` — **GAP:** needs testing under OpenCore.
- In-Setup flash utility (AMI "Instant Flash"-style) from USB as last resort.

### 1.6 Recovery
- Requirement: **dual SPI (A/B) or a protected recovery region** with automatic fallback on failed boot, plus a USB "flashback" (button + USB stick, no CPU/RAM needed) — retail AM5 boards (e.g., ASUS "CrashFree BIOS 3"/BIOS FlashBack, listed on ASUS TUF B650E spec page) prove the pattern exists in AMI ecosystems.
- AMD PSP supports a recovery PSP boot loader entry in the Embedded Firmware Structure (coreboot PSP integration guide). Ask vendor to enable it.
- AM5 requires 256 Mbit (32 MB) SPI for full CPU support (ASUS TUF B650E: "256 Mb Flash ROM"). Budget 2× 32 MB if true dual-flash. **GAP:** AGESA combo images supporting 7000+8000+9000 sometimes drop features to fit 32 MB; ask vendor.
- OS-side recovery is on the ESP (ESP-A/ESP-B/recovery partition), see §3.

### 1.7 Other vendor deliverables
- Full ACPI per §2, incl. our SSDT hooks baked in.
- fTPM 2.0 on by default (Windows 11). Measured boot logs available to Linux.
- S0/S3/S5 and wake: S3 supported (AM5 desktops still use S3; macOS needs S3 for sleep). **GAP:** confirm AGESA image keeps S3 enabled.
- Setup menu: hide advanced options or keep them; "Load MacPro6,2 defaults" must restore D1–D14.
- Source-level access to board port (GPIO, devicetree-equivalent, ACPI ASL) so we can audit; BIOS core/AGESA will remain binary.

---

## 2. ACPI tables and SSDTs for macOS on AM5

Standard tables the BIOS produces (AGESA + IBV): FACP/FADT, DSDT, SSDTs (CPU, PCIe, AMD CPPC), APIC/MADT, MCFG, HPET, FPDT, BGRT, TPM2, IVRS (IOMMU), CRAT/CDIT (AMD topology), WSMT, VFCT (GPU VBIOS for Linux amdgpu, only for iGPU/embedded GPU).

| SSDT / fix | Needed for macOS on AM5? | Bake into ROM? |
|---|---|---|
| SSDT-EC-USBX (fake `EC` device + `USBX` USB power properties) | **Yes** — Dortania lists it as required for all Zen | **Yes.** Vendor adds a `Device (EC)` stub (or real EC named `EC`) and a `USBX` device with `kUSBSleepPortCurrentLimit` etc., gated by `_OSI("Darwin")` so Windows/Linux are unaffected. |
| SSDT-CPUR (CPU objects under `_SB`) | Dortania: only B550/A520. AM5 boards normally declare `Processor`/`Device(ACPI0007)` objects correctly. | **Yes** — require the vendor to declare CPUs as `Device` objects under `\_SB` (ACPI 6.x style). Then no SSDT. **GAP:** verify on sample. |
| USB map (USBMap.kext or SSDT/`_UPC`) | Yes (15-port limit; Dortania: "create a USB map") | **Partly.** Vendor writes accurate `_UPC`/`_PLD` for every port (we give port table). macOS still needs a codeless `USBMap.kext` keyed to our board; ship in OC. |
| SSDT-PLUG / X86PlatformPlugin | No (Intel only) | — |
| SSDT-AWAC / RTC fix | Intel only; AMD has a normal RTC. | — |
| SSDT-SBUS-MCHC | Optional (cosmetic SMBus) | Can bake `MCHC`/`SBUS` stubs. |
| SSDT-PMC | Intel only | — |
| Device names for GPU/audio/NVMe (`GFX0`, `HDEF`) | Helpful for WhateverGreen/AppleALC property injection | **Yes**: name the GPU root port and GPU device consistently. |
| Sleep/wake (`_PRW` 0x0D fix, GPRW) | Often needed on AMD desktops to stop instant wake from USB/LAN | **Yes**: vendor sets correct `_PRW` and lets us choose wake sources. |
| Thunderbolt/USB4 | AM5 USB4 (ASM4242 etc.) is not supported in macOS | Don't put USB4 on the macOS-critical path. |

Rule: anything macOS-only must be wrapped in `If (_OSI ("Darwin"))` so Windows/Linux see standard ACPI. OpenCore also applies ACPI to every OS it boots unless `CustomSMBIOSGuid`/per-OS tricks are used, so baking clean fixes into ROM is better than OC-side patching (Dortania: "our patches are handled by our SSDTs... allow us to boot Windows and other OSes with OpenCore").

---

## 3. OpenCore setup (on the soldered NVMe ESP)

### 3.1 Kernel patches
- AMD_Vanilla `patches.plist` copied into `Kernel > Patch`; requires `Kernel > Quirks > ProvideCurrentCpuInfo = YES` and OpenCore ≥0.7.1 (AMD_Vanilla README).
- **Zen 4/Zen 5 note:** AMD_Vanilla includes an IOPCIFamily patch "required for Zen 4 (Ryzen 7000)" stability (README). Zen 5 coverage: **GAP** — verify the current README/issues for Granite Ridge.
- Core-count patch (`algrey - Force cpuid_cores_per_package`, 4 entries) must contain the **physical core count** of the installed CPU (AMD_Vanilla README table; e.g. 13.3+: `BA <cores> 0000 00`). **This breaks "one config for every SKU".** Mitigations: (a) ship one config per SKU we sell and select at factory; (b) a small OC pre-boot driver or updater that rewrites the value when the CPU changes (**GAP**: doesn't exist publicly); (c) customer CPU swaps need the updater to re-run.
- `Kernel > Emulate > DummyPowerManagement = YES` (Dortania: required for all AMD).
- Quirks per Dortania zen.html: `PanicNoKextDump`, `PowerTimeoutKernelPanic`, `ProvideCurrentCpuInfo` YES; `XhciPortLimit` NO (macOS 11.3+, use USB map).
- Booter quirks: `RebuildAppleMemoryMap`, `SyncRuntimePermissions`, `ResizeAppleGpuBars=0` (since ReBAR is on), `SetupVirtualMap` per sample test (**GAP**), `DevirtualiseMmio` NO.

### 3.2 SMBIOS model
- **MacPro7,1**: Dortania recommends it for AMD Polaris and newer; Navi23 is native under it. It is supported through macOS 26 Tahoe (the last x86 macOS; see firmware-path-evaluation §1.4). iMacPro1,1 is dropped by Tahoe (**GAP:** confirm against Apple's Tahoe compatibility list).
- MacPro7,1 shows "memory misconfigured"/PCIe slot notices on non-Apple boards; RestrictEvents.kext suppresses them (https://github.com/acidanthera/RestrictEvents).
- Identity per unit (serial, MLB, SystemUUID, ROM) generated with `macserial`, never shared (firmware-path-evaluation §2). **Legal GAP** stands.
- `SecureBootModel=Default` (Apple Secure Boot) works with MacPro7,1 (j160) per Dortania Apple Secure Boot page.

### 3.3 Kexts
| Kext | Use | Notes |
|---|---|---|
| Lilu | required base | https://github.com/acidanthera/Lilu |
| VirtualSMC | SMC emulation (required) | https://github.com/acidanthera/VirtualSMC |
| WhateverGreen | Navi23 fixes, `agdpmod=pikera` behaviour | https://github.com/acidanthera/WhateverGreen |
| NootRX | **Not needed.** NootRX is for "unsupported" RDNA2 dGPUs (Navi 22); Navi 23 is native (Dortania). Also note NootRX's ChefKiss licence restricts use; avoid for a commercial product. https://github.com/ChefKissInc/NootRX |
| AMDRyzenCPUPowerManagement | CPU P-state management/idle power | https://github.com/trulyspinach/SMCAMDProcessor — maintainer still calls it not "completely finished". **GAP:** Zen 4/5 support and effect on idle/boost power. |
| SMCAMDProcessor | sensors to VirtualSMC (load after the above) | same repo |
| NVMeFix | APST/power for non-Apple NVMe | https://github.com/acidanthera/NVMeFix |
| USBMap.kext (codeless) | port map for our I/O board | built with USBToolBox/USBMap |
| AppleALC | audio codec on I/O board (if codec is supported) | https://github.com/acidanthera/AppleALC — **choose a codec AppleALC supports** |
| RestrictEvents | MacPro7,1 cosmetic warnings, misc | acidanthera |
| Ethernet | **Pick a NIC with a native or well-supported driver:** Intel i225/i226 → native `AppleIntelI210`-class support is partial; Aquantia AQC107/113 → native in macOS (used by Apple); Realtek RTL8125 → LucyRTL8125Ethernet.kext (third-party). Recommend Aquantia for zero-config. **GAP:** confirm AQC113 native under Tahoe. |
| Wi-Fi/Bluetooth | Intel AX2xx needs itlwm/AirportItlwm + IntelBluetoothFirmware (third-party, no AirDrop); only Broadcom BCM94360-family gets native Continuity but macOS 14+ dropped legacy Broadcom Wi-Fi (OCLP root patch needed). **Decision.** |
| SSDTs | per §2 if not baked in | — |

### 3.4 Known AM5 macOS limitations (flag performance items with ⚡)
- macOS 26 Tahoe is the last x86 release; security updates to ~2028 (firmware-path-evaluation §1.4). Product macOS life is short.
- ⚡ No AMD iGPU acceleration in macOS; dGPU (Navi23) does everything.
- ⚡ CPU power management relies on a third-party kext (AMDRyzenCPUPowerManagement); without it, P-states/idle are firmware-default. Boost behaviour/idle watts under macOS: **GAP**.
- ⚡ Apps that hard-depend on Intel (some Adobe builds use Intel MKL paths, Hypervisor.framework/ Docker Desktop/ Android emulator VMs fail on AMD hackintoshes because AppleHV supports only Intel VT-x). **GAP:** current status for Tahoe; community reports only.
- 32-bit not relevant post-Catalina.
- Core-count patch per SKU (above).
- IOMMU likely off for macOS (above) — conflicts with Windows VBS.
- Sleep/wake must be validated per board; AMD hackintosh sleep is historically fragile.
- USB4/Thunderbolt not usable in macOS on AMD.
- No Apple firmware updates; `BlacklistAppleUpdate=YES`, `run-efi-updater=No` (Dortania).

### 3.5 Boot layout & multi-OS
- As in firmware-path-evaluation §2: ESP-A, ESP-B, recovery partition; `ScanPolicy` set to show internal NVMe/SATA/USB; OpenLinuxBoot for Linux; Windows Boot Manager chainloaded; OC + drivers signed with our db key; Vault on.
- Windows sees OpenCore's SMBIOS unless configured otherwise — ensure Windows activation/OEM licensing keys (MSDM) are not affected. **GAP.**

---

## 4. Driver plan per OS for our boards

| Board | macOS | Windows | Linux |
|---|---|---|---|
| Navi23 GPU board | Native AMDRadeonX6000 if device ID = `73FF`/`73E3`; WhateverGreen + `agdpmod=pikera`; DeviceProperties in OC for our framebuffer port layout (`ATY,Henbury` for Navi23, per perez987 notes: https://github.com/perez987/6600XT-on-macOS-with-softPowerPlayTable/blob/main/README-6600.md). No custom kext if we keep a stock ID. | AMD Adrenalin/Pro driver; needs our subsystem ID accepted (AMD driver INF matches on device ID; custom SSID usually OK). **GAP:** AMD's terms for a board partner custom VBIOS signing. | `amdgpu` upstream; needs firmware blobs (`dimgrey_cavefish`/Navi23 in linux-firmware) — already in distros. |
| I/O board (USB, audio, NIC, Wi-Fi/BT) | USBMap.kext; AppleALC layout ID (submit our layout upstream); NIC per §3.3; Wi-Fi/BT per decision. Anything else → our own signed kext → **needs Apple Developer ID + kext signing approval** (Apple restricts kext signing; DriverKit preferred). **GAP.** | Mostly inbox (USB xHCI, Realtek/Intel NIC); audio via Realtek/HDA inbox or vendor driver; ship via Windows Update (needs Microsoft Partner Center + HLK/attestation signing). | Inbox drivers if we pick upstreamed chips; firmware updates via fwupd. |
| SSD module (NVMe) | Native IONVMeFamily + NVMeFix | inbox `stornvme` | inbox `nvme` |
| Onboard boot NVMe x1 | native | inbox | inbox; ESP mounted read-only by default to avoid accidental edits |
| Fans/sensors/LEDs (if on I/O board via SMBus/EC) | VirtualSMC plugin (ours) | small service + driver | hwmon driver (upstream) |

Principle: **choose chips with inbox drivers in all three OSes**; the only "driver" we then ship is config (OC DeviceProperties, USB map, AppleALC layout).

---

## 5. Path to AMD partnership / IBV engagement (public info only)

What is public:
- AMD's reference BIOS for Ryzen/Threadripper has historically been AMI Aptio V (AMI, 2017: https://www.ami.com/resources/amd-ryzen-aptiov/). Retail AM5 boards ship AMI firmware (e.g. ASUS TUF B650E spec page: "UEFI AMI BIOS").
- Insyde publicly supports AMD embedded parts (InsydeH2O for EPYC Embedded 2005, 2025-12-09: https://www.insyde.com/news/press-releases/insyde-software-ignites-next-generation-embedded-performance-with-uefi-bios-support-for-amd-epyc-embedded-2005-series/).
- **AMD Partner Network for Embedded Partners** (https://www.amd.com/en/partner/partner-network/embedded-partners.html): tiers Registered/Silver/Gold/Platinum; acceptance requires a business model aligned with AMD, quality/technical processes, and AMD sponsorship. This is the most plausible door for a small maker.
- **Ryzen Embedded 9000 is AM5**, Zen 5, up to 16 cores, 28 PCIe Gen5 lanes, 7-year availability (PRO SKUs 10-year), "last order 2033" for the 9950X (https://www.amd.com/en/products/embedded/ryzen/9000-series.html ; https://www.amd.com/en/blogs/2025/amd-ryzen-embedded-9000-series-brings-next-gen-performa.html ; https://www.amd.com/ko/products/embedded/ryzen/9000-series/ryzen-embedded-9950x.html ; Phoronix: https://www.phoronix.com/news/AMD-Ryzen-Embedded-9000-Series). Embedded SKUs are sold through embedded distribution channels that come with BIOS support via IBVs. **Recommendation:** approach AMD as an embedded/small-volume customer on Ryzen Embedded 9000 (same socket, same board), not the consumer channel. Retail Ryzen 7000/9000 chips would still work in the same socket if the AGESA image includes them (**GAP**).

Routes, cheapest-risk first:
1. **ODM route:** contract a Taiwan/China board ODM that already ships AM5 boards (they hold AMD + AMI/Insyde agreements). We own the PCB design; the ODM supplies a customised AMI BIOS under their licence. Lowest legal barrier; we lose source control and depend on their update cadence. **GAP:** which ODMs take small runs; contact only with Aidan's approval.
2. **Embedded board-vendor route:** industrial board makers (e.g. those listed as AMD embedded partners) do custom carrier/full boards on Ryzen Embedded with Insyde/AMI. Similar to ODM, with longer support.
3. **IBV direct:** license AMI Aptio V or InsydeH2O + engineering services. AMI/Insyde require proof of AMD access (AGESA is delivered by AMD to the customer/IBV under NDA). Needs AMD sponsorship first.
4. **AMD direct:** apply to the Embedded Partner Network as Registered tier; ask the sponsor for AGESA/PI access for Ryzen Embedded 9000. Likely needs volume commitments. **GAP:** minimums, fees, timeline (none public).
- How small makers have done it publicly: Framework (Insyde BIOS on AMD laptops, via ODM Compal/Quanta-style partner), System76 and Star Labs (Star Labs ships AMD "Byte Cezanne" with coreboot, see coreboot change 93456, i.e., AMD gave open-firmware access for older APUs). **GAP:** public statements on how Framework got AMD BIOS access; I didn't cite one.

Rough timeline (inference): ODM route 6–12 months to production BIOS once contract signed; IBV/AMD-direct 12–24+ months incl. getting accepted (firmware-path-evaluation §3).

---

## 6. Risks and decisions for Aidan (⚡ = affects performance)

| # | Item | Options / note |
|---|---|---|
| R1 | AMD access may be refused at our volume (**blocker**) | ODM route vs embedded-partner application vs fall back to 8000G/coreboot. **Decision: which route to pursue first** (no contact made). |
| R2 | ⚡ Ryzen Embedded 9000 vs retail 7000/9000 | Embedded = long life + embedded support channel; retail = cheaper, user-upgradable. Same socket. **Decision.** |
| R3 | Core-count kernel patch per CPU SKU | Ship per-SKU configs + updater tool; CPU swaps need re-run. **Decision: allow user CPU upgrades?** |
| R4 | ⚡ IOMMU default | Off = Dortania-safe for macOS; On = Windows VBS/DMA protection and Linux VFIO. **Decision**, pending test (GAP). |
| R5 | ⚡ ReBAR on | Better Windows/Linux GPU perf; macOS needs `ResizeAppleGpuBars=0`. Recommend On. |
| R6 | ⚡ macOS CPU power via third-party kext | Unknown idle/boost behaviour; may cost perf or power in macOS. Benchmark on sample. |
| R7 | ⚡ macOS lifespan (Tahoe last x86) | Product's macOS story ends ~2028 security support. **Decision: is macOS a headline feature?** |
| R8 | Navi23 device ID | Use native `73FF`/`73E3` ID (zero-config) vs custom ID (needs spoof). Recommend native. |
| R9 | NIC/Wi-Fi/BT/audio chip choice | Drives "no user config" across OSes. Recommend Aquantia NIC + AppleALC-supported codec; Wi-Fi is a trade-off. **Decision.** |
| R10 | Apple-format serials / macOS EULA / shipping preinstalled OpenCore | Legal exposure (Apple v. Psystar precedent). **Decision + legal review.** |
| R11 | Secure Boot with our keys + Microsoft certs, key custody | Need HSM/key ceremony; certificate rollover (MS 2011→2023). **Decision: who holds keys.** |
| R12 | Update redistribution (LVFS/Windows Update) depends on IBV/AMD licence | GAP until contract. |
| R13 | 32 MB SPI + dual flash BOM cost | Recommend dual SPI or flashback MCU. **Decision.** |
| R14 | Licence of community kexts (e.g. NootRX licence restrictions; most acidanthera kexts are BSD-3) | Do an OSS licence audit before shipping; avoid NootRX. |
| R15 | ⚡ PCIe lanes | Ryzen 9000 = 28 Gen5 lanes (24 usable + 4 to chipset): x16 GPU + x4 SSD module + x4 chipset; onboard boot x1 must hang off the chipset. Fits. Navi23 only uses x8 Gen4 anyway (**GAP** for our board). |

## 7. Open GAP list (consolidated)
MSR list for AMDRyzenCPUPowerManagement; IOMMU-on macOS boot; `SetupVirtualMap` on AM5; CPU object style in AGESA ACPI; S3 retained in AGESA image; 32 MB combo image limits; AMD GOP redistribution; OC reading identity from firmware SMBIOS; capsule from macOS under OC; Zen 5 coverage in AMD_Vanilla; iMacPro1,1/MacPro7,1 Tahoe list; Hypervisor/Docker on AMD under Tahoe; AQC113 native in Tahoe; AMD/IBV/ODM terms, minimums, timelines; how Framework obtained AMD BIOS; LVFS redistribution permission; Windows OEM activation under OC SMBIOS; kext signing for any custom macOS driver; Apple serial legality.
