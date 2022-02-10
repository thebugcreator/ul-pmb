regular_letters = "abcdefghijklmnopqrstuvwxyz"
french_letters = "éàèùâêîôûçëïüœ"
considered_letters = regular_letters + french_letters

general_sing_titles = {"Monsieur", "Madame", "Mademoiselle"}
general_abbr_titles = {"M.", "Mme", "Mlle"}
general_plu_titles = {"Messieurs", "Mesdames", "Mesdemoiselles"}
general_titles = general_sing_titles.union(general_abbr_titles)

pro_sing_titles = {"Docteur", "Maître", "Professeur"}
pro_abbr_titles = {"Dr", "Me", "Pr"}
pro_titles = pro_sing_titles.union(pro_abbr_titles)

religious_sing_titles = {"Frère", "Mère", "Père", "Révérend Père", "Saint", "Sainte", "Sœur"}
religious_abbr_titles = {"F.", "M.", "P.", "R.P.", "St", "Ste", "Sr"}
religious_titles = religious_sing_titles.union(religious_abbr_titles)

obsolete_sing_titles = {"Monseigneur", "Veuve", "Votre Majesté", "Sa Majesté"}
obsolete_abbr_titles = {"Mgr.", "Vve", "V.M.", "S.M."}
obsolete_titles = obsolete_sing_titles.union(obsolete_abbr_titles)