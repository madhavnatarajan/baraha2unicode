
# \VAR{ prapaataka['title'].strip() }    #
_\VAR{prapaataka['invocation'].strip()}_

## \VAR{prapaataka['sectionTitle'].strip()} ##


\BLOCK{ for anuvakkam in prapaataka['Anuvakkam']}
\BLOCK{ for panchasat in anuvakkam['Panchasat']}
*** \VAR{ panchasat['header'].strip()} ***
\VAR{ panchasat['SamhitaPaata'].strip() }  _\VAR{ panchasat['id']}_


\BLOCK{ if panchasat.get("upaPanchasat") }
*** \VAR{ panchasat['UpaPanchasat']['header'].strip()} ***
\VAR{ panchasat['upaPanchasat']['SamhitaPaata'].replace("\n","").strip()} \newline
\BLOCK{ endif }
                
                
\BLOCK{ if panchasat.get("specialKorvai") }
                
\VAR{ panchasat['specialKorvai'].replace("\n","").strip()}


\BLOCK{ endif }
\BLOCK{endfor}


***(A\VAR{ anuvakkam['Korvai']} \textbf{\VAR{ anuvakkam['anuvakkam_id']}})***


\BLOCK{endfor}

*** \VAR{ prapaataka['PrasnaKorvai_header'].strip()} ***


\VAR{prapaataka['PrasnaKorvai_Sloka'].replace("\n","").strip()}


*** \VAR{ prapaataka['Korvai_header'].strip()} ***


\VAR{ prapaataka['Korvai_Sloka'].replace("\n","").strip()}


*** \VAR{ prapaataka['firstLastPadams_header'].strip()} ***


\VAR{ prapaataka['firstLastPadams_Sloka'].strip()}



\BLOCK{ if prapaataka.get("specialKorvai") }
    
\VAR{ prapaataka['specialKorvai'].replace("\n","").strip()}
\BLOCK{ endif }

\VAR{ prapaataka['ending'].strip() } \newline


\BLOCK{ if prapaataka.get("Appendix") }
\VAR{ prapaataka['Appendix'].replace("\n","\\\\").strip()}
\BLOCK{ endif }

        


\end{document}

