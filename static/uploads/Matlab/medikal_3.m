x= dicomread("ID_0023_AGE_0061_CONTRAST_1_CT.dcm");
imshow(x,[])
dicominfo("ID_0023_AGE_0061_CONTRAST_1_CT.dcm")
x1=imnoise(x,'salt & pepper',0.01);
imshow(x1)
x2=imnoise(x,'gaussian',0.1);
imshow(x2,[])


subplot(1,3,1);
imshow(x,[])
subplot(1,3,2);
imshow(x1,[])
subplot(1,3,3);
imshow(x2,[])