%Makes a list of the 6 neighbors of k,l,m
function retval=neigh(k,l,m,L)
 retval=zeros(6,3);
 retval(1,:)=[mod(k,L)+1 l m];
 retval(2,:)=[mod(k-2,L)+1 l m];
 retval(3,:)=[k mod(l,L)+1 m];
 retval(4,:)=[k mod(l-2,L)+1 m];
 retval(5,:)=[k l mod(m,L)+1];
 retval(6,:)=[k l mod(m-2,L)+1];
endfunction
