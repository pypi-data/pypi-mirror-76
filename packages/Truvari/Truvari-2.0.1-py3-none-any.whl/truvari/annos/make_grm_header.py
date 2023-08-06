#header = my_vcf.header.copy()
    #header.add_line(('##INFO=<ID=TruScore,Number=1,Type=Float,'
                     #'Description="Truvari score for similarity of match">'))
header = []
for prefix in ["rup_", "rdn_", "aup_", "adn_"]:
        for key in ["nhits", "avg_q", "avg_ed", "avg_mat", "avg_mis", "dir_hits", "com_hits", "max_q",
                    "max_ed", "max_mat", "max_mis", "max_strand",
                    "min_q", "min_ed", "min_mat", "min_mis", "min_strand"]:
            header.append(prefix + key)

print(",".join(header))
