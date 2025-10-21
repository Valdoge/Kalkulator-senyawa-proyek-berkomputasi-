#Masukkan data
N=int(input("Masukkan banyak elemen:"))
#Masukkan array pertama
while True:
    print("Masukkan nilai data D1 (tiap elemen pisahkan dengan spasi) hanya 1 atau -1")
    D1=list(map(int, input().split()))
    if len(D1)==N and all (ayam_goreng in (-1,1) for ayam_goreng in D1):
        break
    print("input salah")
#Masukkan array kedua
while True:
    print("Masukkan nilai data D2 (tiap elemen pisahkan dengan spasi) hanya 1 atau -1")
    D2=list(map(int, input().split()))
    if len(D2)==N and all (ikan_goreng in (-1,1) for ikan_goreng in D2):
        break
    print("input salah")

#Formula perhitungan
TP=TN=FP=FN=0
for i in range (N):
    if D1[i]==1 and D2[i]==1:
        TP +=1
    elif D1[i]==-1 and D2[i]==-1:
        TN +=1
    elif D1[i]==-1 and D2[i]==1:
        FP +=1
    elif D1[i]==1 and D2[i]==-1:
        FN +=1

Akurasi=(TP+TN)/(TP+TN+FP+FN)

#output
print("Nilai TP adalah",TP)
print("Nilai TN adalah",TN)
print("Nilai FP adalah",FP)
print("Nilai FN adalah",FN)
print("Akurasi=",Akurasi)