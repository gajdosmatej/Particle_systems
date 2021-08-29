%For a matrix X, choose a pair of indices [i j] according to the normalized
%probability X(i,j).
function retval=pick2(X)
 i=pick1(sum(X,2));
 j=pick1(X(i,:));
 retval=[i j];
endfunction
