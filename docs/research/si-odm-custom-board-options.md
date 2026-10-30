# Custom AM5 board: ODM / module options (SI & Fab, 2026-10-29, research only)
Nobody has contacted any vendor. Any outreach goes through Communications.

## Key findings
- **ASRock Industrial** offers full ODM work: board design, joint validation and controlled production (LOVOT robot case study: https://www.asrockind.com/en-gb/case-study/47). It already ships an AM5 / B650 Ryzen Embedded 7000 Mini-ITX board, the IMB-A1002 (https://www.asrockind.com/en-gb/article/199). Distributor Avnet Silica advertises "light-touch modifications to fully custom designs" (https://my.avnet.com/silica/solutions/compute-modules-sbcs-displays/embedded-compute/asrock/). MOQ, NRE and whether they take individuals are not public. Their customers are OEMs.
- **Advantech** makes the AIMB-723, an AM5 / B650 ATX board for Ryzen Embedded 7000/9000 with AMI BIOS (https://www.advantech.com/en-us/products/5f275228-3385-4034-b102-3bc63b149d4e/aimb-723/mod_8f24f4d6-8036-41cf-9fb5-85b51d43bdcf). It is an AMD Premier partner. Its customization service exists, but MOQ and NRE are not public.
- **AMD partner list** (https://www.amd.com/en/products/embedded/ecosystem.html):
  - Premier: Advantech, Kontron.
  - Elite: congatec, iBase.
  - Select: ASRock, DFI, E.E.P.D., Sapphire, IEI, Lanner.
- **AMD's rules:** partners must sign the Partner Program Agreement and a mutual NDA, and design docs sit on the login-only Embedded Developer Site. Joining needs AMD sales sponsorship and a business survey, so an individual realistically can't get AM5 platform design docs. This backs up why we want a licensed board maker for the BIOS.
- **ASRock Rack, Kontron, DFI, IEI, AAEON, Sapphire, Supermicro, Gigabyte, MSI IPC:** I found no public custom AM5 terms. MOQ, NRE and individual acceptance are not public for all of them.
- **BIOS:** vendor boards ship with AMI UEFI (AIMB-723 and ADLINK cExpress-R8 pages). A custom ODM board would come with the vendor's licensed AMI/Insyde port as part of the NRE. Pricing is not public.

## Alternative: buy a CPU module and design only the carrier board
The module vendor supplies the BIOS and the CPU/DDR fanout. Our board becomes a carrier, and our 1080A/Gen5 work moves to Gen4 on the carrier.
- **COM Express Type 6 Compact (95 × 95 mm), Ryzen Embedded 8000 (Zen 4, 8C/16T, 15–54 W, PCIe Gen4, x16 max):**
  - congatec conga-TCR8: https://www.congatec.com/us/products/com-express-type-6/conga-tcr8/
  - ADLINK cExpress-R8: https://www.adlinktech.com/products/computer_on_modules/comexpresstype6compact/cexpress-r8 (x8 + 8 × x1 Gen4, AMI BIOS)
  - Advantech SOM-6873: https://www.advantech.com/en-us/products/e5f3ee70-5c26-4757-93f4-a9d4150a860f/som-6873/mod_1d0156b1-61b6-48fb-b768-549bb1be3c1c
  - Tria C6C-RYZ8: https://www.tria-technologies.com/2025/03/11/tria-com-express-type-6-module-c6c-ryz8/
  - SECO SOM-COMe-CT6-R8000: https://edge.seco.com/en/products/modules/?edge_cputp=5493
  - SolidRun R8000 COM6: https://my.avnet.com/silica/products/new-products/npi/2026/solidrun-ryzen-r8000-com6-compact/
- **COM-HPC Client Size C (160 × 120 mm), Ryzen AI Embedded X100 (up to 16 Zen 5 cores, 45–120 W, 24 × PCIe Gen4, soldered LPDDR5x up to 128 GB):**
  - congatec: https://www.congatec.com/it/technologies/com-hpc-client-size-c-module-with-amd-ryzentm-ai-embedded-x100-series-processors/
  - ARBOR COMX-C710: https://www.arbor-technology.com/en/new/ARBO-Launches-COMX-C710-AI-Module-Powered-by-AMD-Ryzen-AI-Embedded-X100-Processors-for-Robotics-and-Physical-AI-Applications
- I found no COM-HPC module with a Ryzen Embedded 7000 or 8000 chip.
- Trade-offs:
  - No socketed Ryzen 7000/9000, and no Gen5.
  - The 160 × 120 mm COM-HPC C module must fit the cylinder (Mechanical & Thermal to check).
  - Modules can be bought one at a time through distributors.
  - Carrier design guides from PICMG and the vendors are public or easy to get.

## Ranking for an individual, low-volume build
1. **COM-HPC X100 module plus our own carrier.** This is the best realistic path.
   - Pros: no AMD NDA, BIOS included, up to 16 Zen 5 cores, buyable in single units.
   - Cons: not AM5 or socketed, Gen4 only, soldered RAM, size fit still to check. Moving off socketed AM5 / Gen5 changes performance, so the choice is Aidan's.
2. **Ask ASRock Industrial (via Avnet Silica or MCTX) or Advantech about a semi-custom AM5 board** based on the IMB-A1002 or AIMB-723 design.
   - Pros: real AM5, licensed AMI BIOS, Gen5.
   - Cons: OEM-focused, so likely to require MOQ and NRE (not public) and a business entity. A cylinder-shaped board is a full custom job, not a light modification.
3. **COM Express R8000 module (Zen 4, 8 cores).** This is the low-risk fallback: the cheapest, most widely available option with many vendors, but lower performance.

## Next steps (all through Communications; nothing contacted yet)
- An inquiry to ASRock Industrial (via its product inquiry form at asrockind.com, or Avnet Silica / MCTX at module-store.com) and to Advantech. Ask whether they take individuals or low volume, their MOQ, NRE, BIOS terms, and whether they would do a custom outline from our KiCad design.
- Carrier design guides and single-unit pricing for the congatec and ARBOR X100 COM-HPC modules.
- Mechanical & Thermal to check whether a 160 × 120 mm module fits the 6,1 core.
