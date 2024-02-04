
# \VAR{prasna['section'].strip()} #

_\VAR{prasna['invocation'].strip()}_


\BLOCK{ for anuvakkam in prasna['Anuvakkam']}
\BLOCK{ for panchasat in anuvakkam['Panchasat']}

***\VAR{ panchasat['header'].strip()}***


\VAR{ panchasat['PadaPaata'].strip() }  _\VAR{ panchasat['panchasatInfo']}_ 

\BLOCK{endfor}


\VAR{ anuvakkam['KorvaiInfo']} _\VAR{ anuvakkam['anuvakkamInfo']}_


\BLOCK{endfor}

***{\VAR{ prasna['PrasnaKorvai_header'].strip()}}***


_\VAR{prasna['PrasnaKorvai_Sloka'].replace("\n","").strip()}_

***\VAR{ prasna['Korvai_header'].strip()}***


_\VAR{ prasna['Korvai_Sloka'].replace("\n","").strip()}_



***\VAR{ prasna['firstLastPadams_header'].strip()}***


_\VAR{ prasna['firstLastPadams_Sloka'].strip()}_


\BLOCK{ if prasna.get("specialKorvai_header") }


***\VAR{ prasna['specialKorvai_header'].strip()}***


_\VAR{ prasna['specialKorvai_Sloka'].replace("\n","").strip()}_


\BLOCK{ endif }


***\VAR{ prasna['ending'].strip() }***


\BLOCK{ if prasna.get("Appendix") }


***\VAR{ prasna['Appendix'].strip()}***


\BLOCK{ endif }

