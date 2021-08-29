%For a 3D matrix X, choose a triple of indices [i j k] according to the
%normalized probability X(i,j,k).
function retval=pick3(X)
 i=pick1(sum(sum(X,3),2));
 j=pick1(sum(X(i,:,:),3));
 k=pick1(X(i,j,:));
 retval=[i j k];
endfunction
