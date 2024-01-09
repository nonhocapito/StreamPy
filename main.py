import csv
import os

def interpolazione(lista, v1, v2, k):
    vf=v2+k*(v1-v2)
    return vf

cwd=os.getcwd()
print("Scegli:\t[1] Aria;\n\t[2] Acqua.\n")
test=True
while test==True:
    n=int(input("Inserire un valore: "))
    if n==1:
        name="air"
        sub="aria"
        exp=4   #esponente della viscosità cinematica dell'aria (riga 81)
        test=False
    else:
        if n==2:
            name="water"
            sub="acqua"
            exp=6   #esponente della viscosità cinematica dell'acqua (riga 81)
            test=False
        else:
            print("Valore non valido!")

csv_path=os.path.join(cwd, f"{name}.csv")
file=open(csv_path, newline="")
table=csv.reader(file)

#creo una lista per ogni colonna della tabella
T_list=[]
rho_list=[]
c_list=[]
mu_list=[]
ni_list=[]
kt_list=[]
pr_list=[]

for row in table:
    T_list.append(float(row[0]))
    rho_list.append(float(row[1]))
    c_list.append(float(row[2]))
    mu_list.append(float(row[3]))
    ni_list.append(float(row[4]))
    kt_list.append(float(row[5]))
    pr_list.append(float(row[6]))

#leggo le temperature minima e massima
T_inf=T_list[0] #temperatura limite inferiore
T_sup=T_list[-1]    #temperatura limite superiore
cond=True
while cond==True:
    #input temperatura di film
    Tf=float(input("Inserire una temperatura [°C]: "))

    if Tf>=T_inf and Tf<=T_sup:
        if Tf in T_list:
            i=T_list.index(Tf)
            rho=rho_list[i]
            c=c_list[i]
            mu=mu_list[i]
            ni=ni_list[i]
            kt=kt_list[i]
            pr=pr_list[i]
            
        else:
            for j in range(len(T_list)):
                if Tf>T_list[j]:
                    i=j
                k=(T_list[i+1]-Tf)/(T_list[i+1]-T_list[i])
                rho=round(interpolazione(rho_list, rho_list[i], rho_list[i+1], k), 3)
                c=round(interpolazione(c_list, c_list[i], c_list[i+1], k), 3)
                mu=round(interpolazione(mu_list, mu_list[i], mu_list[i+1], k), 3)
                ni=round(interpolazione(ni_list, ni_list[i], ni_list[i+1], k), 3)
                kt=round(interpolazione(kt_list, kt_list[i], kt_list[i+1], k), 4)
                pr=round(interpolazione(pr_list, pr_list[i], pr_list[i+1], k), 3)    

        print(f"\nProprietà dell'{sub} a {Tf}°C:\n\n\
        ρ = {rho} kg/m3\t\t[densità]\
        \n\tcp = {c} kcal/kg°C\t[calore specifico a pressione costante]\
        \n\tμ = {mu}x10^-5 kg/ms\t[viscosità dinamica]\
        \n\tν = {ni}x10^-{exp} m2/s\t[viscosità cinematica]\
        \n\tk = {kt} kcal/hm°C\t[conducibilità termica]\
        \n\tPr = {pr}\t\t[numero di Prandtl]")
        print(80*"-","\n")

    else:
        if Tf>T_sup:
            print(f"\n\tValore troppo alto (max {T_sup} °C).\n")
        elif Tf<T_inf:
            print(f"\n\tValore troppo basso (min {T_inf} °C).\n")
