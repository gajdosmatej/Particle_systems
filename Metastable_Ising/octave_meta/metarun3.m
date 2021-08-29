time=0;
while time<step
 time=time+1/Rtot;    %time runs proportional to the sum of all rates
 cor=pick4(R);        %pick a site proportional to the rate
 k=cor(1);
 l=cor(2);
 m=cor(3);
 j=cor(4);
 De=-2*X(k,l,m,j);           %change in spin value
 X(k,l,m,j)=X(k,l,m,j)+De;   %flip the spin
 Rnewa=exp(-X(k,l,m,1)*(bet*M(k,l,m,1)/6-al*X(k,l,m,2)));  %new rate at site
 Rnewb=exp(-X(k,l,m,2)*(bet*M(k,l,m,2)/6+al*X(k,l,m,1)));  %new rate at site
 Rtot=Rtot-R(k,l,m,1)-R(k,l,m,2)+Rnewa+Rnewb;              %new sum of rates
 R(k,l,m,1)=Rnewa;           %calculate new rates at site
 R(k,l,m,2)=Rnewb;           %calculate new rates at site
 nn=neigh(k,l,m,L);          %six neighboring sites
 for i=1:6
  kk=nn(i,1);
  ll=nn(i,2);
  mm=nn(i,3);
  M(kk,ll,mm,j)=M(kk,ll,mm,j)+De;  %new magnetization 
  if j==1
   Rnew=exp(-X(kk,ll,mm,1)*(bet*M(kk,ll,mm,1)/6-al*X(kk,ll,mm,2)));
  else
   Rnew=exp(-X(kk,ll,mm,2)*(bet*M(kk,ll,mm,2)/6+al*X(kk,ll,mm,1)));
  end
  Rtot=Rtot-R(kk,ll,mm,j)+Rnew;    %new sum of rates
  R(kk,ll,mm,j)=Rnew;              %new rate at neighboring site
 end
end

Q=(X+1)/2+1;
Pic=makepic(Q,2);
imshow(Pic)
