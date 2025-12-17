x= imread("ID_0068_AGE_0072_CONTRAST_0_CT.tif");
imshow(x)

y1= fft2(x);
y2=abs(y1);
y3= fftshift(y2);
y4= log10(y3);
imshow(y4,[])

z1= ifft2(y1);
imshow(z1)

