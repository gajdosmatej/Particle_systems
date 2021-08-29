bet=3;          %values like 2 or 3 are OK
al=1;
L=30; 		%size of the box
inran=0;        %1 for random initial state, 0 for constant initial state.
step=0.3;         %time step

if inran==1  %random initial state
 X=2*round(rand(L,L,L,2))-ones(L,L,L,2);
else         %completely aligned initial state
 X=ones(L,L,L,2);
end

M=zeros(L,L,L,2);        %local magnetization
R=zeros(L,L,L,2);        %local flip rate
for k=1:L
 for l=1:L
  for m=1:L
   nn=neigh(k,l,m,L);     %coordinates of the 6 neighboring sites
   for i=1:6
    M(k,l,m,:)=M(k,l,m,:)+X(nn(i,1),nn(i,2),nn(i,3),:);
   end
   M(k,l,m,:)=M(k,l,m,:);
   R(k,l,m,1)=exp(-X(k,l,m,1)*(bet*M(k,l,m,1)/6-al*X(k,l,m,2)));
   R(k,l,m,2)=exp(-X(k,l,m,2)*(bet*M(k,l,m,2)/6+al*X(k,l,m,1)));
  end
 end
end

Rtot=squeeze(sum(sum(sum(sum(R,4),3),2),1));   %total flip rate

Q=(X+1)/2+1;
Pic=makepic(Q,2);
imshow(Pic)
