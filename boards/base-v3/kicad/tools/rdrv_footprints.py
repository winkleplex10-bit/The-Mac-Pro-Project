# Footprints for Gen5 redrivers from public TI datasheets (2026-10-28).
import uuid
P='MP62_BP.pretty/'
def U(): return str(uuid.uuid4())
def txt(kind,val,x,y,layer,hide=False):
    return f'  (property "{kind}" "{val}" (at {x} {y} 0) (layer "{layer}") {"(hide yes) " if hide else ""}(uuid "{U()}") (effects (font (size 0.8 0.8) (thickness 0.12))))\n'
def rect(x0,y0,x1,y1,layer,w=0.1):
    return f'  (fp_rect (start {x0} {y0}) (end {x1} {y1}) (stroke (width {w}) (type solid)) (fill no) (layer "{layer}") (uuid "{U()}"))\n'
def gtext(t,x,y,layer,s=0.6):
    return f'  (fp_text user "{t}" (at {x} {y} 0) (layer "{layer}") (uuid "{U()}") (effects (font (size {s} {s}) (thickness 0.1))))\n'
# ---- DS320PR810 NJX0064A WQFN-64, SNLS668 p.34 outline / p.35 land pattern
def njx():
    s=f'(footprint "TI_NJX0064A_WQFN-64_5.5x10mm_P0.4mm_EP4.1x8.6mm" (version 20241229) (generator "pcbnew") (generator_version "9.0") (layer "F.Cu")\n'
    s+='  (descr "TI NJX0064A WQFN-64 5.5x10 mm, 0.4 mm pitch, EP 4.1x8.6 mm. Source: DS320PR810 datasheet SNLS668 (Aug 2022) p.34 package outline, p.35 example land pattern (pads 0.6x0.2, land extents 5.3x9.8). Thermal-via array per p.35 not drawn (add at layout).")\n  (attr smd)\n'
    s+=txt('Reference','REF**',0,-6.2,'F.SilkS')+txt('Value','DS320PR810',0,6.2,'F.Fab')
    s+=txt('Footprint','',0,0,'F.Fab',True)+txt('Datasheet','https://www.ti.com/lit/ds/symlink/ds320pr810.pdf',0,0,'F.Fab',True)+txt('Description','',0,0,'F.Fab',True)
    pads=''
    # pins 1-23 left side top->bottom, x=-2.35 ; 24-32 bottom left->right y=+4.6 ; 33-55 right bottom->top ; 56-64 top right->left
    for i in range(23):
        n=1+i; y=-4.4+0.4*i; pads+=f'  (pad "{n}" smd roundrect (at -2.35 {y:.2f}) (size 0.6 0.2) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (uuid "{U()}"))\n'
    for i in range(9):
        n=24+i; x=-1.6+0.4*i; pads+=f'  (pad "{n}" smd roundrect (at {x:.2f} 4.6 90) (size 0.6 0.2) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (uuid "{U()}"))\n'
    for i in range(23):
        n=33+i; y=4.4-0.4*i; pads+=f'  (pad "{n}" smd roundrect (at 2.35 {y:.2f}) (size 0.6 0.2) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (uuid "{U()}"))\n'
    for i in range(9):
        n=56+i; x=1.6-0.4*i; pads+=f'  (pad "{n}" smd roundrect (at {x:.2f} -4.6 90) (size 0.6 0.2) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25) (uuid "{U()}"))\n'
    pads+=f'  (pad "65" smd rect (at 0 0) (size 4.1 8.6) (layers "F.Cu" "F.Mask") (uuid "{U()}"))\n'
    for x in (-1.0,1.0):
        for y in (-3.45,-1.15,1.15,3.45):
            pads+=f'  (pad "" smd rect (at {x} {y}) (size 1.6 1.9) (layers "F.Paste") (uuid "{U()}"))\n'
    s+=pads+rect(-2.75,-5.05,2.75,5.05,'F.Fab')+rect(-3.0,-5.25,3.0,5.25,'F.CrtYd',0.05)
    s+=f'  (fp_circle (center -3.0 -4.9) (end -2.85 -4.9) (stroke (width 0.15) (type solid)) (fill yes) (layer "F.SilkS") (uuid "{U()}"))\n'
    s+=')\n'; open(P+'TI_NJX0064A_WQFN-64_5.5x10mm_P0.4mm_EP4.1x8.6mm.kicad_mod','w').write(s)
# ---- DS320PR1601 ZDG0354A nFBGA-354 PLACEHOLDER (outline only; ball coordinates not derived)
def zdg():
    s=f'(footprint "TI_ZDG0354A_nFBGA-354_22.9x8.9mm" (version 20241229) (generator "pcbnew") (generator_version "9.0") (layer "F.Cu")\n'
    s+='  (descr "PLACEHOLDER, NOT FOR FAB. TI ZDG0354A nFBGA-354, body 22.8 (22.7-22.9) x 8.9 (8.8-9.0) mm, 1.4 mm max height, ball 0.37 mm, NSMD land 0.30 mm. Source: DS320PR1601 datasheet SNLS683 (Jun 2023) p.40 outline, p.41 example land pattern, p.42 stencil. GAP: 354 ball X/Y coordinates are on a staggered non-uniform grid (0.6 typ / 0.3 offset) and were NOT transcribed; pads must come from TI CAD data (Ultra Librarian) or a full transcription of p.41 before routing. Heatsink keep-out drawn on Dwgs.User for 7.0 W max (SNLS683 p.16 PACT EQ 5-19).")\n  (attr smd)\n'
    s+=txt('Reference','REF**',0,-6.5,'F.SilkS')+txt('Value','DS320PR1601',0,0,'F.Fab')
    s+=txt('Footprint','',0,0,'F.Fab',True)+txt('Datasheet','https://www.ti.com/lit/ds/symlink/ds320pr1601.pdf',0,0,'F.Fab',True)+txt('Description','',0,0,'F.Fab',True)
    s+=rect(-11.45,-4.45,11.45,4.45,'F.Fab')+rect(-11.95,-4.95,11.95,4.95,'F.CrtYd',0.05)+rect(-11.6,-4.6,11.6,4.6,'F.SilkS',0.12)
    s+=f'  (fp_circle (center -11.9 -4.9) (end -11.7 -4.9) (stroke (width 0.15) (type solid)) (fill yes) (layer "F.SilkS") (uuid "{U()}"))\n'
    s+=rect(-12.0,-5.3,12.0,5.3,'Dwgs.User',0.15)+gtext('HEATSINK KO 7 W (24x10.6 band, height TBD M&T)',0,-3.2,'Dwgs.User',0.6)
    s+=gtext('PLACEHOLDER: no balls (GAP, SNLS683 p.41)',0,2.5,'F.Fab',0.7)
    s+=')\n'; open(P+'TI_ZDG0354A_nFBGA-354_22.9x8.9mm.kicad_mod','w').write(s)
# ---- PT5161L fallback: separate alternate footprint, outline only, DNP
def pt():
    s=f'(footprint "Astera_PT5161L_ALT_DNP_PLACEHOLDER" (version 20241229) (generator "pcbnew") (generator_version "9.0") (layer "F.Cu")\n'
    s+='  (descr "DNP fallback alternate site for an Astera Labs PT5161L Gen5 x16 retimer. Package, land pattern, pinout and power are NDA-gated (not public); NO pads drawn, NO pin compatibility with DS320PR1601 assumed (TI publishes no PT5161L cross-map). Outline is a reservation equal to the U20 heatsink band; replace with vendor data via Communications bot.")\n  (attr smd exclude_from_pos_files exclude_from_bom dnp)\n'
    s+=txt('Reference','REF**',0,6.0,'Dwgs.User')+txt('Value','PT5161L_ALT_DNP',0,0,'Dwgs.User')
    s+=txt('Footprint','',0,0,'F.Fab',True)+txt('Datasheet','NDA',0,0,'F.Fab',True)+txt('Description','',0,0,'F.Fab',True)
    s+=f'  (fp_rect (start -12.0 -5.3) (end 12.0 5.3) (stroke (width 0.15) (type dash)) (fill no) (layer "Dwgs.User") (uuid "{U()}"))\n'
    s+=gtext('ALT: PT5161L retimer DNP (land pattern NDA, unverified)',0,0,'Dwgs.User',0.6)
    s+=')\n'; open(P+'Astera_PT5161L_ALT_DNP_PLACEHOLDER.kicad_mod','w').write(s)
njx(); zdg(); pt(); print('ok')
