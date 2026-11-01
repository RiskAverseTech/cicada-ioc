# Stream keys at the cumulative page position (lane C11) under the free-null decoder

Registration: `results/quorum_checks_registration.md` (C11). 583 streams (580 non-periodic pnotisdev streams, three prime streams) at offsets 0.90·cum_k − 50 … cum_k + 50 for each page k (41,420 page-offsets; cum_54 = 12,880), 3 signs × 2 F; tier 1 on the first 160 runes at z ≥ 4.5, tier 2 on the full page at z_uni ≥ 6 and free − plain ≥ 20 nats and readable. **144,887,160 window decodes.** Chance maximum of z over that many tests about 6.1.

## Controls (six plants at the cumulative offset of a page, §62's filler form)

| id | page | stream | sign | F | planted offset | top offset | z1 | rank | z2 | free − plain | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|
| control-00 | LP2-05 | pn:sha256-chain mod :7 | sub | 0 | 1207 | 1206 | 8.0 | 1 | 12.1 | +203 | yes |
| control-01 | LP2-14 | pn:sha256-ctr mod :all things should be encrypted | add | 0 | 3466 | 3466 | 7.4 | 1 | 7.5 | +85 | yes |
| control-02 | LP2-23 | pn:sha512-ctr mod :1729 | beaufort | 0 | 5506 | 5506 | 7.6 | 1 | 9.6 | +140 | yes |
| control-03 | LP2-32 | pn:md5-ctr mod :an instruction | sub | 1 | 7839 | 7839 | 8.4 | 1 | 8.6 | +75 | yes |
| control-04 | LP2-41 | pn:md5-ctr reject :a warning | add | 1 | 9871 | 9871 | 9.3 | 1 | 12.7 | +148 | yes |
| control-05 | LP2-51 | pn:sha256-ctr mod :know this | beaufort | 1 | 12114 | 12111 | 6.1 | 1 | 6.1 | +67 | yes |

Controls passing: 6 of 6.

## Sweep

Largest tier-1 z: 6.79. Tier-1 survivors (z ≥ 4.5): 5,631. Candidates: 38.

- **pn:md5-ctr reject :an end** page LP2-11 add F=True offset 2673: z_uni 6.02, free − plain +134: `THNUIRWULDXWBOEPNFLOHNGRTEEEJEIMBYACUSUDCLRGUCPTHTAOSHNNLMPERYTPFANADEPLOLEOLIFWIHUI`
- **pn:md5-ctr reject :2014** page LP2-39 sub F=False offset 8493: z_uni 6.13, free − plain +168: `EBNTHRNUYSFOLIGOCIUOANUWRUMTHAOOURIAMSRNADSRERUESERNNBNAEIAEIYGGLTSUBAIANWIAMTRSAYTHWNY`
- **pn:md5-ctr reject :2014** page LP2-39 sub F=True offset 8489: z_uni 6.08, free − plain +77: `PSUWELSIOEALIINGDRETTHPDAIASEDWTHNGAFSDENGUADSRERUESERNFYNAEIAEIYGGLTSUBAIANWIAMTRSAYTHWNY`
- **pn:md5-ctr reject :2014** page LP2-39 sub F=True offset 8493: z_uni 6.25, free − plain +137: `EBNTHRNUYSFOLIGOCIUOANUWRUMTHAOOURIAMSRNADSRERUESERNFYNAEIAEIYGGLTSUBAIANWIAMTRSAYTHWNY`
- **pn:md5-ctr reject :2014** page LP2-55 add F=False offset 11864: z_uni 6.16, free − plain +39: `UEABNLOEESEYSCLBOOOCTEDDUPSWTUTTHENGLEOUDULCUIAERISAUYDOPTHFRINESAWEEUEADODEAAOWTHLS`
- **pn:md5-ctr reject :2014** page LP2-55 add F=True offset 11864: z_uni 6.05, free − plain +21: `UEABNLOEESEYSCLBOOOCTEDDUPSWTUTTHENGLEOUDULCUIAERISAUYDOPTHFRINESAWEEUEADODEAAOWTHLS`
- **pn:sha256-ctr mod :self-reliance** page LP2-21 add F=False offset 4644: z_uni 6.01, free − plain +129: `HHRFUNNLLANSYRAXRTMOSTHEUANETCBSRMIUWAEMJEHSOCEMTFIEFAASTHLLEIHTOPWRSIPLINHWEDWHWB`
- **pn:sha256-ctr mod :self-reliance** page LP2-21 add F=False offset 4645: z_uni 6.02, free − plain +134: `BUCUUNNLLANSYRAXRTMOSTHEUANETCBSRMIUWAEMJEHSOCEMTFIEFAASTHLLEIHTOPWRSIPLINHWEDWHWB`
- **pn:sha256-ctr mod :program your mind** page LP2-15 beaufort F=False offset 3592: z_uni 6.04, free − plain +83: `SUUEFRMNNEAXWIHNMWOIPETHIDWRENUIYIHLDIUUTHTHFFTIIAHPUOTXYCATHGSSRUUTHIALRWRTHMSOHGSRIUI`
- **pn:sha256-ctr mod :program your mind** page LP2-15 beaufort F=True offset 3592: z_uni 6.11, free − plain +38: `SUUEFRMNNEAXWIHNMWOIPETHIDWRENUIYIHLDIUUTHTHFFTIIAHPUOTXYCATHGSSRUUTHIALRWRTHMSOHGSRIUI`
- **pn:sha256-ctr mod :program your mind** page LP2-15 beaufort F=True offset 3595: z_uni 6.00, free − plain +46: `FWRPNGOWUAAUWIHNMWOIPETHIDWRENUIYIHLDIUUTHTHFFTIIAHPUOTXYCATHGSSRUUTHIALRWRTHMSOHGSRIUI`
- **pn:sha256-ctr mod :program your mind** page LP2-25 add F=False offset 5340: z_uni 6.15, free − plain +203: `PIWUXEYTMEEYPESJWEIOHEYOLRESBNETHHDPGSBIFEWNETFEILRUIOAFEAOANUEDNICCEICUTEFIOLAMHM`
- **pn:sha256-ctr mod :program your mind** page LP2-25 add F=False offset 5341: z_uni 6.06, free − plain +152: `NIGUXEYTMEEYPESJWEIOHEYOLRESBNETHHDPGSBIFEWNETFEILRUIOAFEAOANUEDNICCEICUTEFIOLAMHM`
- **pn:sha256-ctr mod :program your mind** page LP2-25 add F=True offset 5340: z_uni 6.33, free − plain +147: `PIWUXEYTMEEYPESJWEIOHEYOLRESBNETHHDPGSBIFEWNETFEILRUIOAFEAOANUEDNICCEICUTEFIOLAMHM`
- **pn:sha256-ctr mod :program your mind** page LP2-25 add F=True offset 5341: z_uni 6.25, free − plain +137: `NIGUXEYTMEEYPESJWEIOHEYOLRESBNETHHDPGSBIFEWNETFEILRUIOAFEAOANUEDNICCEICUTEFIOLAMHM`
- **pn:sha256-ctr mod :program your mind** page LP2-25 add F=True offset 5342: z_uni 6.02, free − plain +152: `NOGLYAEYSEEYPESJWEIOHEYOLRESBNETHHDPGSBIFEWNETFEILRUIOAFEAOANUEDNICCEICUTEFIOLAMHM`
- **pn:sha256-ctr reject :pilgrim** page LP2-44 add F=False offset 9859: z_uni 6.06, free − plain +138: `LUMMYYBUOONNBEEABNSNTHCRCEHYLHOIGINGUSOPHURLSDURELWENHEOAITTOLOFNGBYIEIEEYMAEENUUIWOAT`
- **pn:sha256-ctr reject :pilgrim** page LP2-44 add F=False offset 9861: z_uni 6.03, free − plain +144: `TUUIYINOEOONNBEEABNSNTHCRCEHYLHOIGINGUSOPHURLSDURELWENHEOAITTOLOFNGBYIEIEEYMAEENUUIWOAT`
- **pn:sha256-ctr reject :0x7A35090F** page LP2-15 beaufort F=False offset 3307: z_uni 6.53, free − plain +99: `WBONGACRXMEEAGECSEEADONGULOETTHIAPETSNNBTTUAGWOTHEHSDHSYGIIALLBAIACMTTHTHEIOHDYIOIHATBRT`
- **pn:sha256-ctr reject :0x7A35090F** page LP2-15 beaufort F=False offset 3308: z_uni 6.54, free − plain +104: `EUONGACRXMEEAGECSEEADONGULOETTHIAPETSNNBTTUAGWOTHEHSDHSYGIIALLBAIACMTTHTHEIOHDYIOIHATBRT`
- **pn:sha256-ctr reject :0x7A35090F** page LP2-15 beaufort F=False offset 3309: z_uni 6.49, free − plain +99: `DILFNTHIOEMEEAGECSEEADONGULOETTHIAPETSNNBTTUAGWOTHEHSDHSYGIIALLBAIACMTTHTHEIOHDYIOIHATBRT`
- **pn:sha256-ctr reject :0x7A35090F** page LP2-15 beaufort F=False offset 3311: z_uni 6.26, free − plain +104: `MOIBMIOOEOWUAYONSNAFNGILOETTHIAPETSNNBTTUAGWOTHEHSDHSYGIIALLBAIACMTTHTHEIOHDYIOIHATBRT`
- **pn:sha256-ctr reject :0x7A35090F** page LP2-15 beaufort F=False offset 3312: z_uni 6.11, free − plain +129: `RFTAAIOOEOWUAYONSNAFNGILOETTHIAPETSNNBTTUAGWOTHEHSDHSYGIIALLBAIACMTTHTHEIOHDYIOIHATBRT`
- **pn:sha256-ctr reject :0x7A35090F** page LP2-15 beaufort F=True offset 3307: z_uni 6.50, free − plain +81: `WBONGACRXMEEAGECSEEADONGULOETTHIAPETSNNBTTUAGWOTHEHSDHSYGIIALLBAIACMTTHTHEIOHDYIOIHATBRT`
- **pn:sha256-ctr reject :0x7A35090F** page LP2-15 beaufort F=True offset 3308: z_uni 6.52, free − plain +82: `EUONGACRXMEEAGECSEEADONGULOETTHIAPETSNNBTTUAGWOTHEHSDHSYGIIALLBAIACMTTHTHEIOHDYIOIHATBRT`
- **pn:sha256-ctr reject :0x7A35090F** page LP2-15 beaufort F=True offset 3309: z_uni 6.46, free − plain +76: `DILFNTHIOEMEEAGECSEEADONGULOETTHIAPETSNNBTTUAGWOTHEHSDHSYGIIALLBAIACMTTHTHEIOHDYIOIHATBRT`
- **pn:sha256-ctr reject :0x7A35090F** page LP2-15 beaufort F=True offset 3310: z_uni 6.31, free − plain +76: `FILFNTHIOEMEEAGECSEEADONGULOETTHIAPETSNNBTTUAGWOTHEHSDHSYGIIALLBAIACMTTHTHEIOHDYIOIHATBRT`
- **pn:sha256-ctr reject :0x7A35090F** page LP2-15 beaufort F=True offset 3311: z_uni 6.45, free − plain +86: `MOIBMIOOEOWUAYONSNAFNGILOETTHIAPETSNNBTTUAGWOTHEHSDHSYGIIALLBAIACMTTHTHEIOHDYIOIHATBRT`
- **pn:sha256-ctr reject :0x7A35090F** page LP2-15 beaufort F=True offset 3312: z_uni 6.38, free − plain +86: `FOIBMIOOEOWUAYONSNAFNGILOETTHIAPETSNNBTTUAGWOTHEHSDHSYGIIALLBAIACMTTHTHEIOHDYIOIHATBRT`
- **pn:sha256-ctr reject :0x7A35090F** page LP2-15 beaufort F=True offset 3313: z_uni 6.06, free − plain +75: `FFTAAIOOEOWUAYONSNAFNGILOETTHIAPETSNNBTTUAGWOTHEHSDHSYGIIALLBAIACMTTHTHEIOHDYIOIHATBRT`
- **pn:sha256-ctr reject :a warning** page LP2-24 sub F=False offset 5680: z_uni 6.06, free − plain +123: `NIERDWIAIPNYMBARUANETPHBHNWENGTGRGDELLEENTHNGCOFLAITNWYIIWNIUEARGTTAHRREEAELAODDLPAAR`
- **pn:sha512-ctr mod :emergence** page LP2-38 sub F=False offset 8923: z_uni 6.12, free − plain +101: `XRSYDELNIALHIAASEYLTOIMRNESUESNGCYEIWTHGSWLUURLEMIRAGOUMOTHCRCBTEECDTUAESTHIYIISWTHRC`
- **pn:sha512-ctr mod :emergence** page LP2-38 sub F=False offset 8924: z_uni 6.21, free − plain +121: `NAESYDELNIALHIAASEYLTOIMRNESUESNGCYEIWTHGSWLUURLEMIRAGOUMOTHCRCBTEECDTUAESTHIYIISWTHRC`
- **pn:sha512-ctr mod :emergence** page LP2-38 sub F=True offset 8923: z_uni 6.04, free − plain +92: `XRSYDELNIALHIAASEYLTOIMRNESUESNGCYEIWTHGSWLUURLEMIRAGOUMOTHCRCBTEECDTUAESTHIYIISWTHRC`
- **pn:sha512-ctr mod :emergence** page LP2-38 sub F=True offset 8924: z_uni 6.13, free − plain +104: `NAESYDELNIALHIAASEYLTOIMRNESUESNGCYEIWTHGSWLUURLEMIRAGOUMOTHCRCBTEECDTUAESTHIYIISWTHRC`
- **pn:sha512-ctr reject :PILGRIM** page LP2-44 sub F=False offset 9769: z_uni 6.41, free − plain +152: `IPALEOCADIMDICRMOMGAPFERNUCIHIAIEWENUHUUHWTCOOIAEOAOODEOOTHERXCNEISOIHSIABTRYENPOTHWUBU`
- **pn:sha512-ctr reject :PILGRIM** page LP2-44 sub F=True offset 9769: z_uni 6.27, free − plain +129: `IPALEOCADIMDICRMOMGAPFERNUCIHIAIEWENUHUUHWTCOOIAEOAOODEAEFERXCNEISOIHSIABTRYENPOTHWUBU`
- **pn:sha512-ctr reject :know this** page LP2-20 sub F=True offset 4437: z_uni 6.27, free − plain +140: `DDEWDEEOAUPACIDOEOECIAEODNGTEEIOEAGIEFAIYRAFTHFIWATHRLNHMMOAEAIIAOCDHSANEHTLROEMIUJLIDNGYD`

Top tier-1 survivors by full-page z:

| stream | page | sign | F | offset | cum_k | z1 | z2 | free − plain | above null max | transliteration |
|---|---|---|---|---|---|---|---|---|---|---|
| pn:sha256-ctr reject :0x7A35090F | LP2-15 | beaufort | 0 | 3308 | 3603 | 6.8 | 6.54 | +104 | yes | `EUONGACRXMEEAGECSEEADONGULOETTHIAPETSNNBTTUAGWOT` |
| pn:sha256-ctr reject :0x7A35090F | LP2-15 | beaufort | 0 | 3307 | 3603 | 6.8 | 6.53 | +99 | yes | `WBONGACRXMEEAGECSEEADONGULOETTHIAPETSNNBTTUAGWOT` |
| pn:sha256-ctr reject :0x7A35090F | LP2-15 | beaufort | 1 | 3308 | 3603 | 6.4 | 6.52 | +82 | yes | `EUONGACRXMEEAGECSEEADONGULOETTHIAPETSNNBTTUAGWOT` |
| pn:sha256-ctr reject :0x7A35090F | LP2-15 | beaufort | 1 | 3307 | 3603 | 6.4 | 6.50 | +81 | yes | `WBONGACRXMEEAGECSEEADONGULOETTHIAPETSNNBTTUAGWOT` |
| pn:sha256-ctr reject :0x7A35090F | LP2-15 | beaufort | 0 | 3309 | 3603 | 6.7 | 6.49 | +99 | yes | `DILFNTHIOEMEEAGECSEEADONGULOETTHIAPETSNNBTTUAGWO` |
| pn:sha256-ctr reject :0x7A35090F | LP2-15 | beaufort | 1 | 3309 | 3603 | 6.4 | 6.46 | +76 | yes | `DILFNTHIOEMEEAGECSEEADONGULOETTHIAPETSNNBTTUAGWO` |
| pn:sha256-ctr reject :0x7A35090F | LP2-15 | beaufort | 1 | 3311 | 3603 | 6.4 | 6.45 | +86 | yes | `MOIBMIOOEOWUAYONSNAFNGILOETTHIAPETSNNBTTUAGWOTHE` |
| pn:sha512-ctr reject :PILGRIM | LP2-44 | sub | 0 | 9769 | 10690 | 5.0 | 6.41 | +152 | yes | `IPALEOCADIMDICRMOMGAPFERNUCIHIAIEWENUHUUHWTCOOIA` |
| pn:sha256-ctr reject :0x7A35090F | LP2-15 | beaufort | 1 | 3312 | 3603 | 6.3 | 6.38 | +86 | yes | `FOIBMIOOEOWUAYONSNAFNGILOETTHIAPETSNNBTTUAGWOTHE` |
| pn:sha256-ctr mod :program your mind | LP2-25 | add | 1 | 5340 | 5989 | 5.1 | 6.33 | +147 | yes | `PIWUXEYTMEEYPESJWEIOHEYOLRESBNETHHDPGSBIFEWNETFE` |
| pn:sha256-ctr reject :0x7A35090F | LP2-15 | beaufort | 1 | 3310 | 3603 | 6.2 | 6.31 | +76 | yes | `FILFNTHIOEMEEAGECSEEADONGULOETTHIAPETSNNBTTUAGWO` |
| pn:sha512-ctr reject :PILGRIM | LP2-44 | sub | 1 | 9769 | 10690 | 5.0 | 6.27 | +129 | yes | `IPALEOCADIMDICRMOMGAPFERNUCIHIAIEWENUHUUHWTCOOIA` |
| pn:sha512-ctr reject :know this | LP2-20 | sub | 1 | 4437 | 4833 | 5.0 | 6.27 | +140 | yes | `DDEWDEEOAUPACIDOEOECIAEODNGTEEIOEAGIEFAIYRAFTHFI` |
| pn:sha256-ctr reject :0x7A35090F | LP2-15 | beaufort | 0 | 3311 | 3603 | 6.5 | 6.26 | +104 | yes | `MOIBMIOOEOWUAYONSNAFNGILOETTHIAPETSNNBTTUAGWOTHE` |
| pn:md5-ctr reject :2014 | LP2-39 | sub | 1 | 8493 | 9400 | 5.1 | 6.25 | +137 | yes | `EBNTHRNUYSFOLIGOCIUOANUWRUMTHAOOURIAMSRNADSRERUE` |

Coverage limits: the window is 0.90·cum_k − 50 … cum_k + 50 (a filler share above 10 % or skips beyond 50 fall outside); the 580 non-periodic streams and three prime streams only; the free-null decoder at one prior; tier-1 power at 160 runes from §55 part B. Runtime, longest shard: 22.8 h on 8 shards.
