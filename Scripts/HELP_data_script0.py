##HELP Output file parsing for each year and each annual datapoint for precip, runoff, evapotrans, leakage

##Cumulative value columns for precip, ET, and leakage (perc)

import pandas as pd
import numpy as np
import linecache

file = (r"S:\ABQ\Rio_Lisbon_SupplmentalSiteCharacterization\Engineering\FY20-NaturalRecharge-WaterBalance\Models\HELP\Output_Files\Enchanced Tailings\UTB-TP-1\EZD8CN77.txt")


lineNums = []
lines = []
l1 = "ANNUAL TOTALS FOR YEAR"
with open(file) as myfile:
    for num, line in enumerate(myfile, 1):
        if l1 in line:
            print("Year #", num, line)
            lineNums.append(num)
            lines.append(line[51:54])  

lookups_df = pd.DataFrame(lineNums)
lookups_df['Year'] = lines
lookups_df['Year'] = pd.to_numeric(lookups_df['Year'])
lookups_df.columns = ['LineNumber', 'Year']


df_ = lookups_df
df_['precip_line'] = df_.LineNumber + 4
df_['runoff_line'] = df_.LineNumber + 6
df_['evapotrans_line'] = df_.LineNumber + 8
df_['leakage_line'] = df_.LineNumber + 10


df = df_

#precip_vals
pre_range = list(df.precip_line)
precip_vals = []
n=0
for i in pre_range:
    precip_vals.append(pd.to_numeric(linecache.getline(file, df.precip_line[n]).split(" ")[30:32]))
    n +=1

df_p = pd.DataFrame(precip_vals)
df_p1 = df_p
df_p1.columns = ['p1', 'p2']
df_p1.head()
df_p1['New'] = df_p1['p1'].fillna(0) +df_p1['p2'].fillna(0)
precip_values = pd.Series(df_p1['New']).rename("precip_values")
df_['precip_values'] = precip_values

#runoff_vals
runoff_range = list(df.runoff_line)
runoff_vals = []
n=0
for i in runoff_range:
    runoff_vals.append(pd.to_numeric(linecache.getline(file, df.runoff_line[n]).split(" ")[38]))
    n += 1
df_r = pd.DataFrame(runoff_vals) 
df_r.columns = ['runoff_vals']
runoff_values = pd.Series(df_r.runoff_vals).rename("runoff_values")
df_['Runoff_values'] = runoff_values

#evapotrans_vals
et_range = list(df.evapotrans_line)
et_vals = []
n=0
for i in et_range:
    et_vals.append(pd.to_numeric(linecache.getline(file, df.evapotrans_line[n]).split(" ")[25:27]))
    n += 1
df_et = pd.DataFrame(et_vals)
df_et.columns = ['et1', 'et2']
df_et['New'] = df_et['et1'].fillna(0) +df_et['et2'].fillna(0)
et_values = pd.Series(df_et.New).rename("Evapotrans_values")
df_['Evapotrans_values'] = et_values

# leakage_vals
leakage_range = list(df.leakage_line)
leakage_vals = []
n=0
for i in leakage_range:
    leakage_vals.append(pd.to_numeric(linecache.getline(file, df.leakage_line[n]).split(" ")[18]))
    n += 1
leakage_df = pd.DataFrame(leakage_vals)
leakage_df.columns = ['Leakage_vals']
leakage_vals = pd.Series(leakage_df.Leakage_vals).rename("Leakage_vals_in/yr")
df_["Leakage_vals"] = leakage_vals


#preFinal dataframe subset
df_preFinal = df_[['Year',
                  'precip_values',
                  'Runoff_values',
                  'Evapotrans_values',
                  'Leakage_vals']]
                  
#cumulative value columns
df_sums = df_preFinal
df_sums['Cumulative_Precip'] = df_sums['precip_values'].cumsum()
df_sums['Cumulative_ET'] = df_sums['Evapotrans_values'].cumsum()
df_sums['Cumulative_Leakage'] = df_sums['Leakage_vals'].cumsum()

#Export dataframe as .xlsx
#outputfile_name = input("Enter output file name and extension, include .xlsx")

df_sums.to_excel("Help_Output_Dataset0.xlsx", index=False)

print("Script complete. Review output .xlsx file")