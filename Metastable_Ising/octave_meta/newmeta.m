%This simulates "mutually metastable Ising model" in 3 dim. with periodic b.c.
%The program and model are somewhat simplified compared to the script meta.
%At each site i, two spin variables X(i) and Y(i) take values in {-1,+1}.
%FX(i) is the fraction of neighbors j of i for which X(j)=X(i).
%FY(i) is the fraction of neighbors j of i for which Y(j)=Y(i).
%EQ(i) is 1 if X(i)=Y(i) and is 0 otherwise.
%NQ(i) is 0 if X(i)=Y(i) and is 1 otherwise.
%In each step, a site i is chosen uniformly.
%We update with equal probabilities either X or Y.
%X(i) flips with probability exp{-beta*FX(i)-alpha*NQ(i)}.
%Y(i) flips with probability exp{-beta*FY(i)-alpha*EQ(i)}.
%N is the total number of sites.
%The duration of one time step is 1/N.

%The script needs the following functions:
%neigh(k,l,m,L);     %coordinates of the 6 neighboring sites
%XYdraw(X,Y,L);      %draw three sides of a cube in color
%pictperiod          %prepares a movie of 41 frames
%werkperiod          %needed in making pictures
%makepic             %needed in making pictures

begin=clock;

%bet=3, alpha=1, L=5, Tot=10, NT=40, MT=100 takes 1.5 seconds
%bet=3, alpha=1, L=5, Tot=100, NT=40, MT=100 takes 15 seconds
%bet=2, alpha=2, L=5, Tot=1000, NT=40, MT=100 takes 2 min 27 seconds
%bet=3, alpha=2, L=10, Tot=100, NT=40, MT=100 takes 1 min 54 seconds
%bet=3, alpha=2, L=10, Tot=500, NT=40, MT=100 takes 9 min 30 seconds
%bet=3, alpha=1, L=10, Tot=500, NT=40, MT=100 takes 9 min 34 seconds

bet=-4;          %beta; should be larger than 2.65, the critical value.
alpha=1;        %alpha
L=10; 		%length, width and height of the cube
Tot=100; 	%total time
NT=40;		%number of film frames (except initial state) need NT=40
MT=100;         %number of times when mean is recorded

%random initial state
X=2*round(rand(L,L,L))-ones(L,L,L);
Y=2*round(rand(L,L,L))-ones(L,L,L);

%completely aligned initial state
%X=ones(L,L,L);      %initial state (-1,1)
%Y=ones(L,L,L);

N=L*L*L;                   %number of sites
DT=ceil((Tot/NT)*N);       %number of steps of inner loop
dt=Tot/MT;                 %time after which you record total magnetization
rtime=0;                   %running real time
mtel=1;                    %counter for total magnetization

magx=zeros(1,MT+1);   %magnetization of X as a function of time
magy=zeros(1,MT+1);   %magnetization of Y as a function of time

Film{1,1}=XYdraw(X,Y,L);         %record initial state
magx(mtel)=sum(sum(sum(X)))/N;   %record initial magnetization
magy(mtel)=sum(sum(sum(Y)))/N;

for S=1:NT                      %outer loop
 for t=1:DT                     %inner loop
  rtime=rtime+1/N;              %increase real time
  k=ceil(L*rand);               %choose site uniformly
  l=ceil(L*rand);               %choose site uniformly
  m=ceil(L*rand);               %choose site uniformly
  if rand<0.5                   %choose whether X or Y updated
   nn=neigh(k,l,m,L);           %coordinates of the 6 neighboring sites
   MX=0;                        %sum of neighbors with same type
   for i=1:6                    
    kk=nn(i,1);                 
    ll=nn(i,2);
    mm=nn(i,3);
    MX=MX+(X(k,l,m)==X(kk,ll,mm));
   end
   FX=MX/6;                     %fraction of neighbors with same type
   EQ=(X(k,l,m)==Y(k,l,m));     %indicator that X and Y equal
   if rand<exp(-bet*FX-alpha*EQ)
    X(k,l,m)=-X(k,l,m);
   end
  else                          %update Y
   nn=neigh(k,l,m,L);           %coordinates of the 6 neighboring sites
   MY=0;                        %sum of neighbors with same type
   for i=1:6                    
    kk=nn(i,1);                 
    ll=nn(i,2);
    mm=nn(i,3);
    MY=MY+(Y(k,l,m)==Y(kk,ll,mm));
   end
   FY=MY/6;                     %fraction of neighbors with same type
   NQ=(X(k,l,m)!=Y(k,l,m));     %indicator that X and Y not equal
   if rand<exp(-bet*FY-alpha*NQ)
    Y(k,l,m)=-Y(k,l,m);
   end
  end
  if rtime>mtel*dt              %time to record the magnetization
   mtel=mtel+1;
   magx(mtel)=sum(sum(sum(X)))/(L*L*L);
   magy(mtel)=sum(sum(sum(Y)))/(L*L*L);
  end
 end                            %end of the inner loop
 Film{1,S+1}=XYdraw(X,Y,L);     %record the state
end

elaps=etime(clock,begin);       %display the time the program has run
elaps=elaps/(60*60);
hours=floor(elaps)
elaps=60*(elaps-hours);
minutes=floor(elaps)
seconds=60*(elaps-minutes)

magtime=linspace(0,Tot,mtel);   %vector of times when magnetization recorded 
magx=magx(1:mtel);              %due to rounding errors, may have to shorten
magy=magy(1:mtel);

hold off
plot(magtime,magx,'r')          %plot the X-magnetization as a function of time
hold on                       
plot(magtime,magy,'b')

q=0;                            %make a colorful movie
pictperiod

%Now type "makefilm" in your console to create the movie film.pdf
