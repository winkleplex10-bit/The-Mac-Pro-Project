# MacPro6,2 firmware path evaluation (AM5 7000/9000, AM5 8000G, LGA1700)
Date: 2026-10-23. Public sources only. No NDA or leaked material was used. Nothing was pushed or ordered. Anything unverified is marked **GAP**. This builds on `am5-firmware-opencore-research.md`.

## 1. LGA1700 (Alder Lake / Raptor Lake, 12th–14th gen)

### 1.1 Is Intel FSP redistributable?
- **Yes, in binary form.** The FSP_License in github.com/intel/FSP allows "Redistribution and use in binary form, without modification" if you keep the copyright notice and disclaimer. Reverse engineering, decompiling, and disassembling are banned. https://raw.githubusercontent.com/intel/FSP/master/FSP_License.pdf (repo: https://github.com/intel/FSP)
- Dasharo moved its Z690/Z790 builds from the deprecated Alder Lake FSP to the public **Raptor Lake-S client FSP** (v1.1.3, 2024). https://docs.dasharo.com/variants/msi_z690/releases/ and https://blog.3mdeb.com/2024/2024-02-13-msi_z690-a_v1.1.3_release/
- CPU microcode is also a required blob. https://www.phoronix.com/news/Dasharo-1.0-Z690-A-Port
- **GAP: Intel CSME/ME firmware and the flash descriptor.** These are not in intel/FSP. Dasharo's early bring-up pulled microcode from vendor firmware (https://github.com/Dasharo/coreboot/commit/90989b321091a3b7828628304c7cf4bffcc7aed0). I found no public source that lets a new board maker redistribute a production ME image or get the FIT tool without an Intel account or agreement. This is the main LGA1700 licensing unknown.

### 1.2 Retail LGA1700 boards on coreboot/Dasharo today
- **MSI PRO Z690-A (WIFI) DDR4/DDR5:** Dasharo v1.1.7, released 2026-08-13. https://docs.dasharo.com/variants/msi_z690/releases/
- **MSI PRO Z790-P (WIFI) DDR4/DDR5:** Dasharo v0.9.5, released 2026-08-13. https://docs.dasharo.com/variants/msi_z790/releases/ and https://blog.3mdeb.com/2026/2026-08-13-msi_z690-a_z790-p_v1.1.7_v0.9.5_release/
- Both support 12th, 13th, and 14th gen (Raptor Lake Refresh) CPUs, Secure Boot with the Microsoft 2023 certs, capsule/fwupd updates, and turning off the ME. https://docs.dasharo.com/variants/msi_z690/releases/
- Binaries require a Dasharo Pro Package subscription. https://docs.dasharo.com/variants/msi_z790/releases/
- Known issues include Windows not detecting the i225 NIC, VBS not showing as enabled, and some DDR5 XMP1 setups failing to boot. https://docs.dasharo.com/variants/msi_z790/releases/
- **GAP:** I didn't check whether any other retail LGA1700 board has a maintained port.

### 1.3 How hard would a port to our custom LGA1700 board be?
- Upstream coreboot already has `soc/intel/alderlake` with PCH-S support, and the MSI board (ms7d25) is the reference. https://github.com/Dasharo/coreboot/commit/90989b321091a3b7828628304c7cf4bffcc7aed0
- The MSI port took about 2 months, from early support on 2022-04-07 to v1.0 on 2022-06-10, with 3mdeb's core team doing the work on a board with known-good hardware. https://www.phoronix.com/news/Dasharo-1.0-Z690-A-Port
- **Estimate for us (inference):** a port to a new PCB that copies a reference-like PCH-S design would take about 3–6 months to boot, plus 6–12 months to reach production quality (memory compatibility, S3, TPM, updates). Most of the work is the mainboard directory (GPIO, devicetree, DIMM/SPD, Super I/O, EC) plus hardware debugging. Hiring 3mdeb or another firmware house is the realistic route. **GAP: contractor terms and cost.**

### 1.4 How well do Alder Lake / Raptor Lake run macOS?
- **iGPU:** not supported. macOS hasn't supported built-in Intel iGPUs since Rocket Lake, so a supported AMD dGPU is required. https://dortania.github.io/hackintosh/updates/2022/01/09/alder-lake.html
- **E-cores:** OpenCore's `ProvideCurrentCpuInfo` quirk turns on both P- and E-cores, but macOS treats every core as equal. CpuTopologyRebuild.kext rewrites the core layout, and its benefit is uncertain. https://github.com/b00t0x/CpuTopologyRebuild and https://www.reddit.com/r/hackintosh/comments/sp1zgv/opencore_alder_lake_12thgen_intel_hackintosh/
- **Power management:** CFG Lock must be off, or you need the `AppleXcpmCfgLock` quirk. On our own firmware we control the MSR 0xE2 lock, which is an advantage. https://github.com/alyxferrari/OpenCore-Install-Guide/blob/alderlake/config.plist/alder-lake.md **GAP:** I found no measured idle power or XCPM P-state data for ADL/RPL.
- **macOS version limit:** macOS 26 Tahoe is the last release for Intel. macOS 27 runs only on Apple silicon, and Intel security updates continue for about 3 years. https://www.tomshardware.com/software/macos/macos-tahoe-is-the-last-release-for-intel-macs-apple-silicon-exclusivity-will-mark-end-of-hackintoshes , https://www.apple.com/os/macos/ , https://www.heise.de/en/news/macOS-Apple-announces-Intel-security-update-duration-11328845.html
  - **This applies to every x86 option, including AM5.** A macOS-first product has a dead end at Tahoe, with security updates to about 2028.

## 2. Preconfigured OpenCore on a soldered NVMe x1 boot SSD
Design proposal. Each point cites the mechanism it relies on.
- **ESP layout:** use a GPT disk with ESP-A (about 512 MB, FAT32) holding `EFI/OC/{OpenCore.efi,config.plist,Kexts,ACPI,Drivers}` and `EFI/BOOT/BOOTx64.efi`, which is the removable-media fallback path from the UEFI spec. Add ESP-B (a mirror) and a recovery partition. OpenCore layout: https://dortania.github.io/OpenCore-Install-Guide/installer-guide/opencore-efi.html ; UEFI spec: https://uefi.org/specifications
- **Per-unit SMBIOS:** generate serial, MLB, and SystemUUID at the factory with `macserial` (OpenCorePkg/Utilities/macserial), then write them into config.plist or NVRAM per unit. Never ship a shared serial. https://github.com/acidanthera/OpenCorePkg/tree/master/Utilities/macserial and https://dortania.github.io/OpenCore-Post-Install/universal/iservices.html
  - A cleaner option on our own firmware: put the serial and UUID in a write-protected flash region that firmware exposes as SMBIOS, the way Dasharo's ROMHOLE survives updates (https://docs.dasharo.com/variants/msi_z690/releases/). Then set OpenCore `PlatformInfo` `UpdateSMBIOSMode=TryOverwrite`/`Custom` with `Automatic` so config.plist stays identical across units (OpenCore Configuration.pdf: https://github.com/acidanthera/OpenCorePkg/blob/master/Docs/Configuration.pdf). **GAP:** I haven't tested whether OC reads the firmware SMBIOS serial cleanly. **Legal GAP:** whether Apple-format serials and the macOS EULA allow this.
- **Updates from the OS:** OCLP's model of building an EFI and installing it to the ESP from macOS is the closest precedent (https://github.com/dortania/OpenCore-Legacy-Patcher). For us, I'd use a small signed updater, either a macOS pkg or the fwupd/LVFS pattern, that writes ESP-B, checks hashes, and flips the boot order. LVFS/fwupd: https://fwupd.org/ **GAP:** no existing tool does A/B ESP updates for OpenCore.
- **Recovery and fallback ESP:** firmware boot order goes ESP-A, then ESP-B, then removable `BOOTx64.efi`. A hotkey or failed-boot counter in firmware selects ESP-B. OpenCore's own recovery and `ResetNvramEntry` tools are in the OC docs (Configuration.pdf above). A user can also rescue the system from a USB stick with stock OpenCore.
- **Secure Boot with Windows:** Apple Secure Boot (`SecureBootModel`) works on its own (https://dortania.github.io/OpenCore-Post-Install/universal/security/applesecureboot.html). For UEFI Secure Boot, enroll our own db key next to the Microsoft certs and sign OpenCore.efi and its drivers. OpenCore Vault protects config.plist. https://dortania.github.io/OpenCore-Post-Install/universal/security/vault.html ; signing method: https://github.com/perez987/OpenCore-and-UEFI-Secure-Boot . Dasharo already enrolls the Microsoft 2023 keys (https://docs.dasharo.com/variants/msi_z690/releases/).
- **Linux chainloading:** use the OpenLinuxBoot driver (OC 0.7.3+) to boot kernels directly, or chainload shim/GRUB as a picker entry. https://github.com/acidanthera/OpenCorePkg/blob/master/Docs/Configuration.pdf (OpenLinuxBoot section)
- **Why the ESP and not ROM:** an OC or kext update doesn't require a firmware reflash. That avoids the brick and capsule risk covered in the AM5 doc §3.

## 3. Recommended path per CPU option
| CPU option | Firmware path | Timeline (estimate) | Main risks |
|---|---|---|---|
| AM5 Ryzen 7000/9000 | Only a licensed AGESA BIOS through AMI/Insyde or an ODM. Needs an AMD partner NDA (AM5 doc §4). No openSIL support. | 12–24+ months, if AMD accepts us at all | No AMD access at our volume (blocker). Royalties. No public plan for Raphael/Granite Ridge openSIL (AM5 doc §1). |
| AM5 Ryzen 8000G | coreboot + openSIL phoenix_poc + edk2 UEFIPayload, based on the Dasharo MSI B850-P port (https://blog.3mdeb.com/2026/2026-07-30-msi-pro-b850p-v090-release/). OpenCore on the onboard ESP. | 12–18 months with a contractor | openSIL PR still open. Fewer PCIe lanes (GAP). Capsule and S5 bugs. One reference board. Tahoe is the macOS limit. |
| LGA1700 12th–14th | coreboot + public Raptor Lake FSP + edk2. Fork the Dasharo ms7d25/ms7e06 code. OpenCore on the onboard ESP. | About 6–12 months to production with a contractor | ME/descriptor licensing (GAP). No iGPU in macOS. E-core scheduling. Raptor Lake instability needs microcode (GAP: not reviewed here). Tahoe is the macOS limit. |

**Recommendation:** LGA1700 is the only option with publicly redistributable silicon init and a mature retail coreboot reference. It's also the only one where we control CFG Lock. Pick it if macOS is the main target. Keep 8000G as the AMD route. Treat 7000/9000 as impossible without an AMD partnership.
