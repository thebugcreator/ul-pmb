#constants.py : 
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

phrase = {  "qu'est-ce" : ("qu_est_ce",) , "Qu'est-ce" : ("Qu_est_ce", ) ,
			"il y a":("il ", "y ", "a",) , "Il y a":("Il ", "y ", "a",) ,
			"quelques-uns" : ("quelques_uns",) ,  "Quelques-uns" : ("Quelques_uns",) , 
			"quelques-unes" : ("quelques_unes",) , "Quelques-unes" : ("Quelques_unes",) ,
			"faudra-t-il" : ("faudra", "-t_il" ), "Faudra-t-il" : ("Faudra", "-t_il") ,
			"fait-il" : ("fait", "-il") , "Fait-il" : ( "Fait", "-il" ),
			"doit-il" : ("doit", "-il") , "Doit-il" : ("Doit", "-il") ,
			"s'agit-il" : ("s'", "agit",  "il") , "S'agit-il" : ("S'", "agit", "-il" ),
			} 
			# 'il y a':'il_y_a', 'Il y a':'Il_y_a' 
			# [faudra][-t-il]","[fait][-il]","[doit][-il]”, “[s’][agit][-il]

			