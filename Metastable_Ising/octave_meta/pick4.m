%For a 4D matrix X, choose a quadruple of indices [i j k l] according to the
%normalized probability X(i,j,k,l).
function retval=pick4(X)
 i=pick1(sum(sum(sum(X,4),3),2));
 j=pick1(sum(sum(X(i,:,:,:),4),3));
 k=pick1(sum(X(i,j,:,:),4));
 l=pick1(X(i,j,k,:));
 retval=[i j k l];
endfunction
