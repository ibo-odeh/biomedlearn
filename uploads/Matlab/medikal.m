x= imread("ID_0099_AGE_0060_CONTRAST_1_CT.tif");
imshow(x)
imhist(x)
y=dicomFile('ID_0000_AGE_0060_CONTRAST_1_CT.dcm');
y1=dicomread("ID_0000_AGE_0060_CONTRAST_1_CT.dcm");
imshow(y1,[])
imhist(y1)
e=histeq(y1)
subplot(2,1,1)
imshow(y1,[])
title('orjinal')
subplot(2,1,2)
imshow(e)
title('new')


z = imbinarize(y1,"adaptive")
imshow(z)
z1 = edge(y1,"sobel")
imshow(z1)

