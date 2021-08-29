%(X,Y) is (-1,-1) geeft 1=blue
%         (-1,+1) geeft 2=dark blue
%         (+1,+1) geeft 3=red
%         (+1,-1) geeft 4=dark red
function retval=twoXYdraw(X,Y,L)
 X=round(X);
 Y=round(Y);
 retval=3*ones(L,L)+X-(X==Y);
endfunction
