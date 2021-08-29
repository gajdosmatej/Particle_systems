%For a vector x=[x(1) ... x(n)], choose a random index i between 1 and n
%where i is chosen with probability x(i)/sum(x);
function retval=pick1(x)
 N=length(x);
 x=x/sum(x);
 l=0;
 r=length(x);
 L=0;
 R=1;
 rara=rand;
 while r-l>1
  m=l+round((r-l)/2);
  M=L+sum(x(l+1:m));
  if rara<M
   r=m;
   R=M;
  else
   l=m;
   L=M;
  end
 end
 retval=r;
endfunction
