%This simulates "catalytic metastable Ising model" in 3 dim. with periodic b.c.
%At each site i, two spin variables X(i) and Y(i) take values in {-1,+1}
%Local magnetization M_x(i) at site is average of X over 6 nearest neighb.
%X(i) flips at rate exp[-X(i)*{beta*M_x(i)+alpha*Y(i)}]
%Y(i) flips at rate exp[-Y(i)*{beta*M_y(i)-alpha*X(i)}]

%The script needs the following functions:
%neigh(k,l,m,L);     %coordinates of the 6 neighboring sites
%XYdraw(X,Y,L);      %draw three sides of a cube in color
%choose(r);          %pick an index with probab. proportional to r
%pictperiod          %prepares a movie of 41 frames
%werkperiod          %needed in making pictures
%makepic             %needed in making pictures

%When the script finishes, in your console, you run the binscript makefilm.
%You then save the figure as magnet.pdf and finally type
%pdfunite magnet.pdf draw.pdf simulatie_parameters.pdf

begin=clock;

%bet=3, al=1, L=10, Tot=20, MT=40 takes 38 seconds
%bet=3, al=1, L=15, Tot=20, MT=40 takes 2:16
%bet=3, al=1, L=20, Tot=40, MT=100 takes 11:20
%bet=3, al=1, L=30, Tot=40, MT=100 takes [estimated 38:13]

bet=3;          %values like 2 or 3 are OK
al=1;
L=30; 		%size of the box
Tot=40;		%total time
NT=40;		%number of film frames (except initial state) need NT=40
MT=100;         %number of times when mean is recorded
bbet=bet/6;

%random initial state
%X=2*round(rand(L,L,L))-ones(L,L,L);
%Y=2*round(rand(L,L,L))-ones(L,L,L);

%completely aligned initial state
X=ones(L,L,L);      %initial state (-1,1)
Y=ones(L,L,L);

magx=zeros(1,MT+1);   %magnetization of X as a function of time
magy=zeros(1,MT+1);   %magnetization of Y as a function of time

Film{1,1}=XYdraw(X,Y,L);  %record initial state

Mx=zeros(L,L,L);        %local sum of magnetization
My=zeros(L,L,L);        %local sum of magnetization
rrrx=zeros(L,L,L);       %local flip rate of X
rrry=zeros(L,L,L);       %local flip rate of Y
for k=1:L
 for l=1:L
  for m=1:L
   nn=neigh(k,l,m,L);     %coordinates of the 6 neighboring sites
   for i=1:6
    Mx(k,l,m)=Mx(k,l,m)+X(nn(i,1),nn(i,2),nn(i,3));
    My(k,l,m)=My(k,l,m)+Y(nn(i,1),nn(i,2),nn(i,3));
   end
   rrrx(k,l,m)=exp(-X(k,l,m)*(bbet*Mx(k,l,m)+al*Y(k,l,m)));
   rrry(k,l,m)=exp(-Y(k,l,m)*(bbet*My(k,l,m)-al*X(k,l,m)));
  end
 end
end
rrr=rrrx+rrry; %sum of rates for X and Y
rr=sum(rrr,3); %marginal
r=sum(rr,2);   %marginal
R=sum(r);      %sum of all rates

magx(1)=sum(sum(sum(X)))/(L*L*L);
magy(1)=sum(sum(sum(Y)))/(L*L*L);

DT=Tot/NT;       %duration or inner loop
dt=Tot/MT;       %time after which you record total magnetization
rtime=0;           %running time
mtel=1;           %counter for total magnetization

for S=1:NT                      %central loop
 target=S*DT;
 while rtime<target              %inner loop
  rtime=rtime+1/R;                %increase real time
  k=choose(r);                  %choose coordinates proportional to rates
  l=choose(rr(k,:));            %conditional law of l given k
  m=choose(rrr(k,l,:));         %conditional law of m given k and l
  if rand<rrrx(k,l,m)/rrr(k,l,m)  %choose whether X or Y flips
   dM=-2*X(k,l,m);              %local change in magnetization
   X(k,l,m)=-X(k,l,m);          %flip X
   rrrx(k,l,m)=exp(-X(k,l,m)*(bbet*Mx(k,l,m)+al*Y(k,l,m))); %update flip rate
   rrry(k,l,m)=exp(-Y(k,l,m)*(bbet*My(k,l,m)-al*X(k,l,m)));
   rrr(k,l,m)=rrrx(k,l,m)+rrry(k,l,m);
   nn=neigh(k,l,m,L);     %coordinates of the 6 neighboring sites
   for i=1:6              %update magnetization and local flip rate
    kk=nn(i,1);           %for all neighboring sites
    ll=nn(i,2);
    mm=nn(i,3);
    Mx(kk,ll,mm)=Mx(kk,ll,mm)+dM;
    rrrx(kk,ll,mm)=exp(-X(kk,ll,mm)*(bbet*Mx(kk,ll,mm)+al*Y(kk,ll,mm)));
    rrr(kk,ll,mm)=rrrx(kk,ll,mm)+rrry(kk,ll,mm);
   end
  else
   dM=-2*Y(k,l,m);              %local change in magnetization
   Y(k,l,m)=-Y(k,l,m);          %flip Y
   rrrx(k,l,m)=exp(-X(k,l,m)*(bbet*Mx(k,l,m)+al*Y(k,l,m))); %update flip rate
   rrry(k,l,m)=exp(-Y(k,l,m)*(bbet*My(k,l,m)-al*X(k,l,m)));
   rrr(k,l,m)=rrrx(k,l,m)+rrry(k,l,m);
   nn=neigh(k,l,m,L);     %coordinates of the 6 neighboring sites
   for i=1:6              %update magnetization and local flip rate
    kk=nn(i,1);           %for all neighboring sites
    ll=nn(i,2);
    mm=nn(i,3);
    My(kk,ll,mm)=My(kk,ll,mm)+dM;
    rrry(kk,ll,mm)=exp(-Y(kk,ll,mm)*(bbet*My(kk,ll,mm)-al*X(kk,ll,mm)));
    rrr(kk,ll,mm)=rrrx(kk,ll,mm)+rrry(kk,ll,mm);
   end
  end
  rr=sum(rrr,3); %marginal
  r=sum(rr,2);   %marginal
  R=sum(r);      %sum of all rates
  if rtime>mtel*dt
   magx(mtel+1)=sum(sum(sum(X)))/(L*L*L);
   magy(mtel+1)=sum(sum(sum(Y)))/(L*L*L);
   mtel=mtel+1;
  end
 end
 Film{1,S+1}=XYdraw(X,Y,L);
end

elaps=etime(clock,begin);
elaps=elaps/(60*60);
hours=floor(elaps)
elaps=60*(elaps-hours);
minutes=floor(elaps)
seconds=60*(elaps-minutes)

magtime=linspace(0,Tot,mtel);  %mtel zou nu MT+1 moeten zijn als alles goed is

plot(magtime,magx,'r')
%plot(magtime,magy,'b')

q=1;
pictperiod
%makefilm   -in je console runnen


