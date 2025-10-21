sum=0
count=0


N=int(input("Masukkan bilangan bulat:"))
while(N!=-999):
    sum=sum+N
    count=count+1
    N=int(input("Masukkan bilangan bulat:"))

if(count>0):
    rata_rata=(sum/count)
    print("Banyak bilangan =", + str(count))
    print("Jumlah data +", + str(sum))
    print("Nilai rata ratanya adalah", + str(rata_rata))
else:
    print ("Tidak ada data yang diolah")


