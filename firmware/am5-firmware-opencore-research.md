# AM5 CPU board (MacPro6,2): firmware and OpenCore-in-ROM research
Date: 2026-10-23. Public sources only. Uncertain items are marked GAP. No board files were changed.

## 1. openSIL on AM5 desktop
- AMD's public openSIL `phoenix_poc` branch covers **Phoenix only**: Ryzen 8000G APUs, originally mobile. 3mdeb added the AM5 desktop Phoenix support, which is upstream as openSIL PR #58 and still **open** (last updated 2026-08-10). https://github.com/openSIL/openSIL/pull/58
- **There is no public openSIL branch for Raphael (Ryzen 7000) or Granite Ridge (Ryzen 9000).** 3mdeb: "Any other processors are not supported and will not boot." https://blog.3mdeb.com/2026/2026-07-30-msi-pro-b850p-v090-release/
- AMD has said production openSIL replaces AGESA starting with Zen 6 (as reported by PCGH): https://www.pcgameshardware.de/CPU-CPU-154106/News/Dasharo-v0-9-0-Open-Source-BIOS-AM5-Ryzen-8000G-1550495/
- **Boots today:** yes, but only one board with one CPU family. The MSI PRO B850-P WIFI runs Dasharo v0.9.0 (coreboot 25.12, openSIL, edk2 UEFIPayload) and boots Ubuntu 26.04 and Windows 11 25H2 on Ryzen 8000G, validated on an 8600G.
- GAP: no OSFC talk was checked. No AMD statement gives a date for Raphael or Granite Ridge openSIL.

## 2. coreboot on AM5
- The upstream coreboot tree has `soc/amd/phoenix` with `SOC_AMD_PHOENIX_AM5_OPENSIL`. Gerrit change 94664 switches the submodule to the 3mdeb fork, and 94673 adds the PROM21 (B850 chipset) driver. https://mail.coreboot.org/archives/list/coreboot-gerrit@coreboot.org/thread/23P3PZRTRVDS45XAGGVOH46YHQGELIPN/ and https://review.coreboot.org/c/coreboot/+/94673
- The only board is the MSI PRO B850-P (Dasharo, 3mdeb porting series): https://blog.3mdeb.com/2026/2026-04-27-msi_pro_b850p_part4/
- **Zen 4 Raphael / Zen 5 Granite Ridge desktop:** no port exists. 3mdeb says one would need AMD to publish openSIL for those SoCs, and it asks users to register demand on the openSIL GitHub. No AMD plan has been announced (GAP).
- Known Dasharo v0.9.0 issues: UEFI capsule staging across resets, S5 power-state restore, an Ubuntu serial-console hang, and the WiFi card intermittently disappearing.
- **Board impact:** a coreboot route today would only support Ryzen 8000G (Phoenix) in our socket. That excludes 7000/9000 and X3D. Phoenix also has fewer CPU PCIe lanes (GAP: confirm the Phoenix AM5 lane count against our GPU x16 plus NVMe lane plan).

## 3. OpenCore inside firmware
- **Mac Pro 5,1:** OpenCore itself is **not** put in the BootROM. Only the small EnableGop DXE driver, built from OpenCore parts, is injected with DXEInject. It gives a pre-OpenCore boot picker and GOP. Flashing a wrong image bricks the machine. OpenCore still runs from the ESP. https://forums.macrumors.com/threads/enablegop-pre-opencore-gop-support-for-efi-era-imacs-and-mac-pros.2378942/
- **OpenDuet** (OpenCorePkg/Legacy) is a DUET-style UEFI environment loaded from disk boot sectors, not from flash. https://github.com/acidanthera/OpenCorePkg (Legacy/README.md)
- **edk2 UEFIPayload as a coreboot payload** is mainstream. Dasharo uses it. https://github.com/tianocore/edk2/blob/master/UefiPayloadPkg/BuildAndIntegrationInstructions.txt In principle, OpenCore.efi plus its drivers and config could go into the payload FV as a built-in boot option. GAP: no public, maintained project found that ships OpenCore in SPI flash on a PC board, and no reliability data was found.
- **What breaks, from OpenCore's design (inference, not tested):**
  - **NVRAM:** macOS expects working, non-volatile runtime variables. coreboot's SMMSTORE works for edk2, but needs testing with macOS writes.
  - **Apple Secure Boot / SecureBootModel:** works from the ESP today. In ROM it is the same, but UEFI Secure Boot keys for Windows have to coexist.
  - **Updates:** every OpenCore or kext update becomes a full firmware reflash. That is a brick risk, and capsule staging is already a known Dasharo issue.
  - **ACPI:** SSDT patches baked into the ROM can't be fixed per user.
  - **Config:** the config.plist and its SMBIOS serial must be per-unit or generated at runtime. Shipping one serial across units is a legal and Apple-ID problem.
  - **SPI size:** AM5 uses 32 MB (256 Mbit) SPI. OpenCore plus kexts is a few MB, which is probably fine (GAP: measure it).
  - **Legal:** shipping macOS-booting hardware runs into Apple's macOS EULA. Not engineering, but a real risk.

## 4. Commercial closed BIOS (AMI Aptio / Insyde) with AGESA
- AMI licenses Aptio to OEMs under a Software License Agreement plus a Source Code Access Agreement, with per-ROM royalties and quarterly minimum commitments. A redacted congatec agreement is public in SEC filings: https://www.sec.gov/Archives/edgar/data/1648741/000091205715000257/filename3.htm
- The AGESA PI source and binaries for AM5 are given by AMD only to partners under NDA (board vendors, IBVs). An IBV can't sublicense AGESA to a party that has no AMD relationship. GAP: no public AMD document lists entry requirements or minimum volumes.
- AMI's Aptio CommunityEdition is openSIL-based, with no AGESA. It's aimed at OCP server platforms: https://www.ami.com/resources/unlocking-the-future-of-compute-ami-and-amds-collaborative-breakthrough-at-ocp-global-summit-2023/ That route inherits the same openSIL SoC gap for Raphael and Granite Ridge.
- **Verdict:** a licensed AGESA BIOS for Ryzen 7000/9000 is **not possible without an AMD NDA/partner agreement**. It is realistically out of reach at small volumes unless an ODM or IBV takes on the project as a paid engagement. The other route is a firmware house like 3mdeb as a contractor (GAP: their terms).

## 5. Feasibility verdict
| Path | CPUs | Timeline (estimate) | Main risks |
|---|---|---|---|
| A. coreboot + openSIL + UEFIPayload + OpenCore in ROM | 8000G only today | 12–24+ months for a new-board port. The 3mdeb MSI port ran Feb–Jul 2026 with the core team | Raphael/Granite Ridge blocked on AMD; NVRAM, update and brick risk; no reference project |
| B. AMI/Insyde + AGESA, OpenCore as a DXE/boot option | 7000/9000 | 12+ months plus contracts | Needs an AMD NDA; royalties and minimums; IBV may refuse macOS-related work |
| C. **Fallback: soldered boot device with OpenCore preloaded on the x1 link** | All | Weeks (hardware is already planned) | Uses x1 and board area; firmware remains a closed or vendor BIOS |

**Recommendation: C now, with A watched as a future option.** Use a small onboard NVMe (BGA SSD or M.2 2230 on J8's x1 link), or USB-attached eMMC/UFS, holding only a FAT ESP with OpenCore. The UEFI BIOS boots it first, and OpenCore then chains macOS, Windows (bootmgfw) and Linux. That meets "no user config", stays updateable from the OS, and recovers by reflashing the boot device instead of SPI. SPI isn't an option for OpenCore storage unless we own the firmware. eMMC/UFS needs host controller support that AM5 lacks natively (GAP), so NVMe x1 is the simplest.

Path C still has a blocking question (GAP): which UEFI firmware runs on our board at all? The board needs an AGESA BIOS. Without the NDA in section 4, the only buildable firmware today is openSIL/coreboot, and that means Phoenix 8000G.

What we'd need for A: a commercial engagement with 3mdeb or similar, Phoenix-only CPU support (or waiting on AMD), SMMSTORE NVRAM validation with macOS, and a signed update and recovery path (dual SPI or a recovery header).
