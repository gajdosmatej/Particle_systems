%(X,Y) is (-1,-1) geeft 1=blue
%         (-1,+1) geeft 2=dark blue
%         (+1,+1) geeft 3=red
%         (+1,-1) geeft 4=dark red
function retval=XYdraw(X,Y,L)
 X=round(X);
 Y=round(Y);
 color=3*ones(L,L,L)+X-(X==Y);
 up=squeeze(color(:,:,1));
 right=squeeze(color(:,L,:));
 down=squeeze(color(L,:,:))';
 retval=[up right; down zeros(L,L)];
endfunction
