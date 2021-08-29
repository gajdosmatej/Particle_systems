%Creates a color picture from a matrix Q with values in {1,...,q}
%For three-dimensional matrices, three sides of the rectangle are shown.
%If the last dimension is 2, this is interpreted as two values at one site.
%Each value in {1,...,q} gets a color.
%Pictures with q=2 are done in black-and-white
%For q=3,4 the colors are chosen by hand
%For q=5 or more, the idea is to mix the colors as follows.
%You use only colors in the plane R+G+B=3.
%You turn around the point R=G=B=1
%So you let x vary between 0 and 1 and take
%R=1+sin(2*pi*x)       (varies between 0 and 2).
%G=1+sin(2*pi*(x+1/3))
%B=1+sin(2*pi*(x+2/3))
%You allow 256 shades so you round.
%
function retval=makepic(Q,q)
 dim=ndims(Q);
 if size(Q)(dim)==2        %If last dimension 2, interpret as two values.
  double=1;                %records that there are two values
  dim=dim-1;
  if dim==2
   QQ=squeeze(Q(:,:,2));
   Q=squeeze(Q(:,:,1));
  else
   QQ=squeeze(Q(:,:,:,2));
   Q=squeeze(Q(:,:,:,1));
  end
 else
  double=0;                %records that there is only one values
 end
 if dim==3          %show three sides of a rectangle
  C=[zeros(size(Q)(1),size(Q)(2)) zeros(size(Q)(1),size(Q)(3)); %white corner
     zeros(size(Q)(3),size(Q)(2)) ones(size(Q)(1),size(Q)(3))];
  up=squeeze(Q(:,:,1));
  right=squeeze(Q(:,size(Q)(2),:));
  down=squeeze(Q(size(Q)(1),:,:))';
  Q=[up right; down ones(size(Q)(3),size(Q)(3))];
  if double==1
   up=squeeze(QQ(:,:,1));
   right=squeeze(QQ(:,size(QQ)(2),:));
   down=squeeze(QQ(size(QQ)(1),:,:))';
   QQ=[up right; down ones(size(QQ)(3),size(QQ)(3))];
  end
 else
  C=zeros(size(Q)(1),size(Q)(2));  %no white corner
 end
 if double==1
  P=QQ/q;   %second value translated into brightness. Black not used.
 else
  P=ones(size(Q)(1),size(Q)(2));  %all maximally bright
 end
 if min(q==2,double==0)
  R=(Q==2);
  G=(Q==2);
  B=(Q==2);
 end
 if max(min(q==2,double==1),max(q==3,q==4))
  R=(Q==1)+(Q==3);
  G=(Q>2);
  B=(Q==2);
 end
 if q>4
  R=ceil(128*(1+sin(2*pi*(Q/q))))/256;
  G=ceil(128*(1+sin(2*pi*(Q/q+1/3))))/256;
  B=ceil(128*(1+sin(2*pi*(Q/q+2/3))))/256;
 end
 R=P.*R;       %if there are two values, translate second into brightness
 G=P.*G; 
 B=P.*B;
 R=max(C,R);   %in three dim, white corner
 G=max(C,G);
 B=max(C,B);
 T=size(R)(1);
 N=size(R)(2);
 retval=zeros(T,N,3);
 retval(:,:,1)=R;
 retval(:,:,2)=G;
 retval(:,:,3)=B;
endfunction
