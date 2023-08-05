#!/bin/sh

set -eu

similar()
{
	psnr=$(compare -metric PSNR "$1" "$2" null: 2>&1 || true)
	if [ -z "$psnr" ]; then
		echo "compare failed"
		return 1
	fi

	# PSNR of zero means that they are identical
	if [ "$psnr" = 0 ]; then
		echo "images are equal -- don't use similar() but require exactness"
		exit 2
	fi

	# The lower PSNR value, the fewer the similarities
	# The lowest (and worst) value is 1.0
	# head -n == --lines, but more portable (MacOS)
	min_psnr=50
	if [ "$min_psnr" != "$( printf "$psnr\n$min_psnr\n" | sort --general-numeric-sort | head -n1)" ]; then
		echo "pdf wrongly rendered"
		return 1
	fi
	return 0
}

compare_rendered()
{
	pdf="$1"
	img="$2"
	gsdevice=png16m
	if [ "$#" -eq 3 ]; then
		gsdevice="$3"
	fi

	compare_ghostscript "$pdf" "$img" "$gsdevice"

	compare_poppler "$pdf" "$img"

	compare_mupdf "$pdf" "$img"
}

compare_ghostscript()
{
	pdf="$1"
	img="$2"
	gsdevice="$3"
	gs -dQUIET -dNOPAUSE -dBATCH -sDEVICE="$gsdevice" -r96 -sOutputFile="$tempdir/gs-%00d.png" "$pdf"
	compare -metric AE "$img" "$tempdir/gs-1.png" null: 2>/dev/null
	rm "$tempdir/gs-1.png"
}

compare_poppler()
{
	pdf="$1"
	img="$2"
	pdftocairo -r 96 -png "$pdf" "$tempdir/poppler"
	compare -metric AE "$img" "$tempdir/poppler-1.png" null: 2>/dev/null
	rm "$tempdir/poppler-1.png"
}

compare_mupdf()
{
	pdf="$1"
	img="$2"
	mutool draw -o "$tempdir/mupdf.png" -r 96 "$pdf" 2>/dev/null
	if [ "$(uname)" != "Darwin" ]; then  # mupdf is not pixel perfect on Darwin
		compare -metric AE "$img" "$tempdir/mupdf.png" null: 2>/dev/null
	fi
	rm "$tempdir/mupdf.png"
}

compare_pdfimages()
{
	pdf="$1"
	img="$2"
	pdfimages -png "$pdf" "$tempdir/images"
	compare -metric AE "$img" "$tempdir/images-000.png" null: 2>/dev/null
	rm "$tempdir/images-000.png"
}

checkpdf()
{
	python3 -c 'import pikepdf,sys; p=pikepdf.open(sys.argv[1]);exit(sum([not eval("p.pages[0]."+l) for l in sys.stdin]))' "$1"
}

error()
{
	echo test $j failed
	echo intermediate data is left in $tempdir
	exit 1
}

# -d == --directory, -t == --template, but more portable (MacOS, FreeBSD)
tempdir=$(mktemp -d -t img2pdf.XXXXXXXXXX)

trap error EXIT

# instead of using imagemagick to craft the test input, we use a custom python
# script. This is because the output of imagemagick is not bit-by-bit identical
# across versions and architectures.
# See https://gitlab.mister-muffin.de/josch/img2pdf/issues/56
python3 magick.py "$tempdir"

if [ "$(uname)" = "Darwin" ]; then
	status_arg=
else
	status_arg=--status
fi

cat << END | ( cd "$tempdir"; md5sum --check $status_arg - )
cc611e80cde3b9b7adb7723801a4e5d4  alpha.png
706175887af8ca1a33cfd93449f970df  gray16.png
ff4d9f18de39be879926be2e65990167  gray1.png
d51900476658a1c9dd26a7b27db8a21f  gray2.png
722223ba74be9cba1af4a549076b70d3  gray4.png
2320216faa5a10bf0f5f04ebce07f8e1  gray8.png
35a47d6ae6de8c9d0b31aa0cda8648f3  inverse.png
6ad810399058a87d8145d8d9a7734da5  normal16.png
c8d2e1f116f31ecdeae050524efca7b6  normal.png
18a3dfca369f976996ef93389ddfad61  palette1.png
d38646afa6fa0714be9badef25ff9392  palette2.png
e1c59e68a68fca3273b6dc164d526ed7  palette4.png
50bf09eb3571901f0bf642b9a733038c  palette8.png
END

# use img2pdfprog environment variable if it is set
if [ -z ${img2pdfprog+x} ]; then
	img2pdfprog=src/img2pdf.py
fi

available_engines="internal"

if python3 -c "import pdfrw" 2>/dev/null; then
	available_engines="$available_engines pdfrw"
fi
if python3 -c "import pikepdf" 2>/dev/null; then
	available_engines="$available_engines pikepdf"
fi

img2pdf()
{
	$img2pdfprog --producer="" --nodate --engine="$1" "$2" > "$3" 2>/dev/null
}

tests=51 # number of tests
j=1      # current test

###############################################################################
echo "Test $j/$tests JPEG"

convert "$tempdir/normal.png" "$tempdir/normal.jpg"

identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Format: JPEG (Joint Photographic Experts Group JFIF format)$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Mime type: image/jpeg$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Type: TrueColor$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Depth: 8-bit$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Compression: JPEG$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/normal.jpg" "$tempdir/out.pdf"

# We have to use jpegtopnm with the original JPG before being able to compare
# it with imagemagick because imagemagick will decode the JPG slightly
# differently than ghostscript, poppler and mupdf do it.
# We have to use jpegtopnm and cannot use djpeg because the latter produces
# slightly different results as well when called like this:
#    djpeg -dct int -pnm "$tempdir/normal.jpg" > "$tempdir/normal.pnm"
# An alternative way to compare the JPG would be to require a different DCT
# method when decoding by setting -define jpeg:dct-method=ifast in the
# compare command.
jpegtopnm -dct int "$tempdir/normal.jpg" > "$tempdir/normal.pnm" 2>/dev/null

compare_rendered "$tempdir/out.pdf" "$tempdir/normal.pnm"

pdfimages -j "$tempdir/out.pdf" "$tempdir/images"
cmp "$tempdir/normal.jpg" "$tempdir/images-000.jpg"
rm "$tempdir/images-000.jpg"

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 8
Resources.XObject.Im0.ColorSpace == "/DeviceRGB"
Resources.XObject.Im0.Filter == "/DCTDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
rm "$tempdir/out.pdf"
done

rm "$tempdir/normal.jpg" "$tempdir/normal.pnm"
j=$((j+1))

###############################################################################
echo "Test $j/$tests JPEG (90° rotated)"

convert "$tempdir/normal.png" "$tempdir/normal.jpg"
exiftool -overwrite_original -all= "$tempdir/normal.jpg" -n >/dev/null
exiftool -overwrite_original -Orientation=6 -XResolution=96 -YResolution=96 -n "$tempdir/normal.jpg" >/dev/null

identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Format: JPEG (Joint Photographic Experts Group JFIF format)$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Mime type: image/jpeg$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Resolution: 96x96$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Units: PixelsPerInch$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Type: TrueColor$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Depth: 8-bit$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Compression: JPEG$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Orientation: RightTop$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/normal.jpg" "$tempdir/out.pdf"

# We have to use jpegtopnm with the original JPG before being able to compare
# it with imagemagick because imagemagick will decode the JPG slightly
# differently than ghostscript, poppler and mupdf do it.
# We have to use jpegtopnm and cannot use djpeg because the latter produces
# slightly different results as well when called like this:
#    djpeg -dct int -pnm "$tempdir/normal.jpg" > "$tempdir/normal.pnm"
# An alternative way to compare the JPG would be to require a different DCT
# method when decoding by setting -define jpeg:dct-method=ifast in the
# compare command.
jpegtopnm -dct int "$tempdir/normal.jpg" > "$tempdir/normal.pnm" 2>/dev/null
convert -rotate "90" "$tempdir/normal.pnm" "$tempdir/normal_rotated.png"
#convert -rotate "0" "$tempdir/normal.pnm" "$tempdir/normal_rotated.png"

compare_rendered "$tempdir/out.pdf" "$tempdir/normal_rotated.png"

pdfimages -j "$tempdir/out.pdf" "$tempdir/images"
cmp "$tempdir/normal.jpg" "$tempdir/images-000.jpg"
rm "$tempdir/images-000.jpg"

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 8
Resources.XObject.Im0.ColorSpace == "/DeviceRGB"
Resources.XObject.Im0.Filter == "/DCTDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
Rotate == 90
END
rm "$tempdir/out.pdf"
done

rm "$tempdir/normal.jpg" "$tempdir/normal.pnm" "$tempdir/normal_rotated.png"
j=$((j+1))

###############################################################################
echo "Test $j/$tests JPEG CMYK"

convert "$tempdir/normal.png" -colorspace cmyk "$tempdir/normal.jpg"

identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Format: JPEG (Joint Photographic Experts Group JFIF format)$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Mime type: image/jpeg$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Colorspace: CMYK$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Type: ColorSeparation$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Depth: 8-bit$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/normal.jpg" | grep --quiet '^  Compression: JPEG$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/normal.jpg" "$tempdir/out.pdf"

gs -dQUIET -dNOPAUSE -dBATCH -sDEVICE=tiff32nc -r96 -sOutputFile="$tempdir/gs-%00d.tiff" "$tempdir/out.pdf"
similar "$tempdir/normal.jpg" "$tempdir/gs-1.tiff"
rm "$tempdir/gs-1.tiff"

# not testing with poppler as it cannot write CMYK images

mutool draw -o "$tempdir/mupdf.pam" -r 96 -c cmyk "$pdf" 2>/dev/null
similar "$tempdir/normal.jpg" "$tempdir/mupdf.pam"
rm "$tempdir/mupdf.pam"

pdfimages -j "$tempdir/out.pdf" "$tempdir/images"
cmp "$tempdir/normal.jpg" "$tempdir/images-000.jpg"
rm "$tempdir/images-000.jpg"

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 8
Resources.XObject.Im0.ColorSpace == "/DeviceCMYK"
Resources.XObject.Im0.Decode == pikepdf.Array([ 1, 0, 1, 0, 1, 0, 1, 0 ])
Resources.XObject.Im0.Filter == "/DCTDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
rm "$tempdir/out.pdf"
done

rm "$tempdir/normal.jpg"
j=$((j+1))

###############################################################################
echo "Test $j/$tests JPEG2000"

convert "$tempdir/normal.png" "$tempdir/normal.jp2"

identify -verbose "$tempdir/normal.jp2" | grep --quiet '^  Format: JP2 (JPEG-2000 File Format Syntax)$'
identify -verbose "$tempdir/normal.jp2" | grep --quiet '^  Mime type: image/jp2$'
identify -verbose "$tempdir/normal.jp2" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/normal.jp2" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/normal.jp2" | grep --quiet '^  Type: TrueColor$'
identify -verbose "$tempdir/normal.jp2" | grep --quiet '^  Depth: 8-bit$'
identify -verbose "$tempdir/normal.jp2" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/normal.jp2" | grep --quiet '^  Compression: JPEG2000$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/normal.jp2" "$tempdir/out.pdf"

compare_rendered "$tempdir/out.pdf" "$tempdir/normal.jp2"

pdfimages -jp2 "$tempdir/out.pdf" "$tempdir/images"
cmp "$tempdir/normal.jp2" "$tempdir/images-000.jp2"
rm "$tempdir/images-000.jp2"

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 8
Resources.XObject.Im0.ColorSpace == "/DeviceRGB"
Resources.XObject.Im0.Filter == "/JPXDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
rm "$tempdir/out.pdf"
done

rm "$tempdir/normal.jp2"
j=$((j+1))

###############################################################################
#echo Test JPEG2000 CMYK
#
# cannot test because imagemagick does not support JPEG2000 CMYK

###############################################################################
echo "Test $j/$tests PNG RGB8"

identify -verbose "$tempdir/normal.png" | grep --quiet '^  Format: PNG (Portable Network Graphics)$'
identify -verbose "$tempdir/normal.png" | grep --quiet '^  Mime type: image/png$'
identify -verbose "$tempdir/normal.png" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/normal.png" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/normal.png" | grep --quiet '^  Type: TrueColor$'
identify -verbose "$tempdir/normal.png" | grep --quiet '^  Depth: 8-bit$'
identify -verbose "$tempdir/normal.png" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/normal.png" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/normal.png" | grep --quiet '^    png:IHDR.bit-depth-orig: 8$'
identify -verbose "$tempdir/normal.png" | grep --quiet '^    png:IHDR.bit_depth: 8$'
identify -verbose "$tempdir/normal.png" | grep --quiet '^    png:IHDR.color-type-orig: 2$'
identify -verbose "$tempdir/normal.png" | grep --quiet '^    png:IHDR.color_type: 2 (Truecolor)$'
identify -verbose "$tempdir/normal.png" | grep --quiet '^    png:IHDR.interlace_method: 0 (Not interlaced)$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/normal.png" "$tempdir/out.pdf"

compare_rendered "$tempdir/out.pdf" "$tempdir/normal.png"

compare_pdfimages "$tempdir/out.pdf" "$tempdir/normal.png"

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 8
Resources.XObject.Im0.ColorSpace == "/DeviceRGB"
Resources.XObject.Im0.DecodeParms.BitsPerComponent == 8
Resources.XObject.Im0.DecodeParms.Colors == 3
Resources.XObject.Im0.DecodeParms.Predictor == 15
Resources.XObject.Im0.Filter == "/FlateDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
rm "$tempdir/out.pdf"
done

j=$((j+1))

###############################################################################
echo "Test $j/$tests PNG RGB16"

identify -verbose "$tempdir/normal16.png" | grep --quiet '^  Format: PNG (Portable Network Graphics)$'
identify -verbose "$tempdir/normal16.png" | grep --quiet '^  Mime type: image/png$'
identify -verbose "$tempdir/normal16.png" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/normal16.png" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/normal16.png" | grep --quiet '^  Type: TrueColor$'
identify -verbose "$tempdir/normal16.png" | grep --quiet '^  Depth: 16-bit$'
identify -verbose "$tempdir/normal16.png" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/normal16.png" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/normal16.png" | grep --quiet '^    png:IHDR.bit-depth-orig: 16$'
identify -verbose "$tempdir/normal16.png" | grep --quiet '^    png:IHDR.bit_depth: 16$'
identify -verbose "$tempdir/normal16.png" | grep --quiet '^    png:IHDR.color-type-orig: 2$'
identify -verbose "$tempdir/normal16.png" | grep --quiet '^    png:IHDR.color_type: 2 (Truecolor)$'
identify -verbose "$tempdir/normal16.png" | grep --quiet '^    png:IHDR.interlace_method: 0 (Not interlaced)$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/normal16.png" "$tempdir/out.pdf"

compare_ghostscript "$tempdir/out.pdf" "$tempdir/normal16.png" tiff48nc

# poppler outputs 8-bit RGB so the comparison will not be exact
pdftocairo -r 96 -png "$tempdir/out.pdf" "$tempdir/poppler"
similar "$tempdir/normal16.png" "$tempdir/poppler-1.png"
rm "$tempdir/poppler-1.png"

# pdfimages is unable to write 16 bit output

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 16
Resources.XObject.Im0.ColorSpace == "/DeviceRGB"
Resources.XObject.Im0.DecodeParms.BitsPerComponent == 16
Resources.XObject.Im0.DecodeParms.Colors == 3
Resources.XObject.Im0.DecodeParms.Predictor == 15
Resources.XObject.Im0.Filter == "/FlateDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
rm "$tempdir/out.pdf"
done

j=$((j+1))

###############################################################################
echo "Test $j/$tests PNG RGBA8"

convert "$tempdir/alpha.png" -depth 8 -strip "$tempdir/alpha8.png"

identify -verbose "$tempdir/alpha8.png" | grep --quiet '^  Format: PNG (Portable Network Graphics)$'
identify -verbose "$tempdir/alpha8.png" | grep --quiet '^  Mime type: image/png$'
identify -verbose "$tempdir/alpha8.png" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/alpha8.png" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/alpha8.png" | grep --quiet '^  Type: TrueColorAlpha$'
identify -verbose "$tempdir/alpha8.png" | grep --quiet '^  Depth: 8-bit$'
identify -verbose "$tempdir/alpha8.png" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/alpha8.png" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/alpha8.png" | grep --quiet '^    png:IHDR.bit-depth-orig: 8$'
identify -verbose "$tempdir/alpha8.png" | grep --quiet '^    png:IHDR.bit_depth: 8$'
identify -verbose "$tempdir/alpha8.png" | grep --quiet '^    png:IHDR.color-type-orig: 6$'
identify -verbose "$tempdir/alpha8.png" | grep --quiet '^    png:IHDR.color_type: 6 (RGBA)$'
identify -verbose "$tempdir/alpha8.png" | grep --quiet '^    png:IHDR.interlace_method: 0 (Not interlaced)$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/alpha8.png" /dev/null && rc=$? || rc=$?
if [ "$rc" -eq 0 ]; then
	echo needs to fail here
	exit 1
fi
done

rm "$tempdir/alpha8.png"
j=$((j+1))

###############################################################################
echo "Test $j/$tests PNG RGBA16"

identify -verbose "$tempdir/alpha.png" | grep --quiet '^  Format: PNG (Portable Network Graphics)$'
identify -verbose "$tempdir/alpha.png" | grep --quiet '^  Mime type: image/png$'
identify -verbose "$tempdir/alpha.png" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/alpha.png" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/alpha.png" | grep --quiet '^  Type: TrueColorAlpha$'
identify -verbose "$tempdir/alpha.png" | grep --quiet '^  Depth: 16-bit$'
identify -verbose "$tempdir/alpha.png" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/alpha.png" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/alpha.png" | grep --quiet '^    png:IHDR.bit-depth-orig: 16$'
identify -verbose "$tempdir/alpha.png" | grep --quiet '^    png:IHDR.bit_depth: 16$'
identify -verbose "$tempdir/alpha.png" | grep --quiet '^    png:IHDR.color-type-orig: 6$'
identify -verbose "$tempdir/alpha.png" | grep --quiet '^    png:IHDR.color_type: 6 (RGBA)$'
identify -verbose "$tempdir/alpha.png" | grep --quiet '^    png:IHDR.interlace_method: 0 (Not interlaced)$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/alpha.png" /dev/null && rc=$? || rc=$?
if [ "$rc" -eq 0 ]; then
	echo needs to fail here
	exit 1
fi
done

j=$((j+1))

###############################################################################
echo "Test $j/$tests PNG Gray8 Alpha"

convert "$tempdir/alpha.png" -colorspace Gray -dither FloydSteinberg -colors 256 -depth 8 -strip "$tempdir/alpha_gray8.png"

identify -verbose "$tempdir/alpha_gray8.png" | grep --quiet '^  Format: PNG (Portable Network Graphics)$'
identify -verbose "$tempdir/alpha_gray8.png" | grep --quiet '^  Mime type: image/png$'
identify -verbose "$tempdir/alpha_gray8.png" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/alpha_gray8.png" | grep --quiet '^  Colorspace: Gray$'
identify -verbose "$tempdir/alpha_gray8.png" | grep --quiet '^  Type: GrayscaleAlpha$'
identify -verbose "$tempdir/alpha_gray8.png" | grep --quiet '^  Depth: 8-bit$'
identify -verbose "$tempdir/alpha_gray8.png" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/alpha_gray8.png" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/alpha_gray8.png" | grep --quiet '^    png:IHDR.bit-depth-orig: 8$'
identify -verbose "$tempdir/alpha_gray8.png" | grep --quiet '^    png:IHDR.bit_depth: 8$'
identify -verbose "$tempdir/alpha_gray8.png" | grep --quiet '^    png:IHDR.color-type-orig: 4$'
identify -verbose "$tempdir/alpha_gray8.png" | grep --quiet '^    png:IHDR.color_type: 4 (GrayAlpha)$'
identify -verbose "$tempdir/alpha_gray8.png" | grep --quiet '^    png:IHDR.interlace_method: 0 (Not interlaced)$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/alpha_gray8.png" /dev/null && rc=$? || rc=$?
if [ "$rc" -eq 0 ]; then
	echo needs to fail here
	exit 1
fi
done

rm "$tempdir/alpha_gray8.png"
j=$((j+1))

###############################################################################
echo "Test $j/$tests PNG Gray16 Alpha"

convert "$tempdir/alpha.png" -colorspace Gray -depth 16 -strip "$tempdir/alpha_gray16.png"

identify -verbose "$tempdir/alpha_gray16.png" | grep --quiet '^  Format: PNG (Portable Network Graphics)$'
identify -verbose "$tempdir/alpha_gray16.png" | grep --quiet '^  Mime type: image/png$'
identify -verbose "$tempdir/alpha_gray16.png" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/alpha_gray16.png" | grep --quiet '^  Colorspace: Gray$'
identify -verbose "$tempdir/alpha_gray16.png" | grep --quiet '^  Type: GrayscaleAlpha$'
identify -verbose "$tempdir/alpha_gray16.png" | grep --quiet '^  Depth: 16-bit$'
identify -verbose "$tempdir/alpha_gray16.png" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/alpha_gray16.png" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/alpha_gray16.png" | grep --quiet '^    png:IHDR.bit-depth-orig: 16$'
identify -verbose "$tempdir/alpha_gray16.png" | grep --quiet '^    png:IHDR.bit_depth: 16$'
identify -verbose "$tempdir/alpha_gray16.png" | grep --quiet '^    png:IHDR.color-type-orig: 4$'
identify -verbose "$tempdir/alpha_gray16.png" | grep --quiet '^    png:IHDR.color_type: 4 (GrayAlpha)$'
identify -verbose "$tempdir/alpha_gray16.png" | grep --quiet '^    png:IHDR.interlace_method: 0 (Not interlaced)$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/alpha_gray16.png" /dev/null && rc=$? || rc=$?
if [ "$rc" -eq 0 ]; then
	echo needs to fail here
	exit 1
fi
done

rm "$tempdir/alpha_gray16.png"
j=$((j+1))

###############################################################################
echo "Test $j/$tests PNG interlaced"

convert "$tempdir/normal.png" -interlace PNG -strip "$tempdir/interlace.png"

identify -verbose "$tempdir/interlace.png" | grep --quiet '^  Format: PNG (Portable Network Graphics)$'
identify -verbose "$tempdir/interlace.png" | grep --quiet '^  Mime type: image/png$'
identify -verbose "$tempdir/interlace.png" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/interlace.png" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/interlace.png" | grep --quiet '^  Type: TrueColor$'
identify -verbose "$tempdir/interlace.png" | grep --quiet '^  Depth: 8-bit$'
identify -verbose "$tempdir/interlace.png" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/interlace.png" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/interlace.png" | grep --quiet '^    png:IHDR.bit-depth-orig: 8$'
identify -verbose "$tempdir/interlace.png" | grep --quiet '^    png:IHDR.bit_depth: 8$'
identify -verbose "$tempdir/interlace.png" | grep --quiet '^    png:IHDR.color-type-orig: 2$'
identify -verbose "$tempdir/interlace.png" | grep --quiet '^    png:IHDR.color_type: 2 (Truecolor)$'
identify -verbose "$tempdir/interlace.png" | grep --quiet '^    png:IHDR.interlace_method: 1 (Adam7 method)$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/interlace.png" "$tempdir/out.pdf"

compare_rendered "$tempdir/out.pdf" "$tempdir/normal.png"

compare_pdfimages "$tempdir/out.pdf" "$tempdir/normal.png"

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 8
Resources.XObject.Im0.ColorSpace == "/DeviceRGB"
Resources.XObject.Im0.DecodeParms.BitsPerComponent == 8
Resources.XObject.Im0.DecodeParms.Colors == 3
Resources.XObject.Im0.DecodeParms.Predictor == 15
Resources.XObject.Im0.Filter == "/FlateDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
rm "$tempdir/out.pdf"
done

rm "$tempdir/interlace.png"
j=$((j+1))

###############################################################################
for i in 1 2 4 8; do
	echo "Test $j/$tests PNG Gray$i"

	identify -verbose "$tempdir/gray$i.png" | grep --quiet '^  Format: PNG (Portable Network Graphics)$'
	identify -verbose "$tempdir/gray$i.png" | grep --quiet '^  Mime type: image/png$'
	identify -verbose "$tempdir/gray$i.png" | grep --quiet '^  Geometry: 60x60+0+0$'
	identify -verbose "$tempdir/gray$i.png" | grep --quiet '^  Colorspace: Gray$'
	if [ "$i" -eq 1 ]; then
		identify -verbose "$tempdir/gray$i.png" | grep --quiet '^  Type: Bilevel$'
	else
		identify -verbose "$tempdir/gray$i.png" | grep --quiet '^  Type: Grayscale$'
	fi
	if [ "$i" -eq 8 ]; then
		identify -verbose "$tempdir/gray$i.png" | grep --quiet "^  Depth: 8-bit$"
	else
		identify -verbose "$tempdir/gray$i.png" | grep --quiet "^  Depth: 8/$i-bit$"
	fi
	identify -verbose "$tempdir/gray$i.png" | grep --quiet '^  Page geometry: 60x60+0+0$'
	identify -verbose "$tempdir/gray$i.png" | grep --quiet '^  Compression: Zip$'
	identify -verbose "$tempdir/gray$i.png" | grep --quiet "^    png:IHDR.bit-depth-orig: $i$"
	identify -verbose "$tempdir/gray$i.png" | grep --quiet "^    png:IHDR.bit_depth: $i$"
	identify -verbose "$tempdir/gray$i.png" | grep --quiet '^    png:IHDR.color-type-orig: 0$'
	identify -verbose "$tempdir/gray$i.png" | grep --quiet '^    png:IHDR.color_type: 0 (Grayscale)$'
	identify -verbose "$tempdir/gray$i.png" | grep --quiet '^    png:IHDR.interlace_method: 0 (Not interlaced)$'

	for engine in $available_engines; do
	img2pdf $engine "$tempdir/gray$i.png" "$tempdir/out.pdf"

	compare_rendered "$tempdir/out.pdf" "$tempdir/gray$i.png" pnggray

	compare_pdfimages "$tempdir/out.pdf" "$tempdir/gray$i.png"

	cat << END | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == $i
Resources.XObject.Im0.ColorSpace == "/DeviceGray"
Resources.XObject.Im0.DecodeParms.BitsPerComponent == $i
Resources.XObject.Im0.DecodeParms.Colors == 1
Resources.XObject.Im0.DecodeParms.Predictor == 15
Resources.XObject.Im0.Filter == "/FlateDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
	rm "$tempdir/out.pdf"
	done

	j=$((j+1))
done

###############################################################################
echo "Test $j/$tests PNG Gray16"

identify -verbose "$tempdir/gray16.png" | grep --quiet '^  Format: PNG (Portable Network Graphics)$'
identify -verbose "$tempdir/gray16.png" | grep --quiet '^  Mime type: image/png$'
identify -verbose "$tempdir/gray16.png" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/gray16.png" | grep --quiet '^  Colorspace: Gray$'
identify -verbose "$tempdir/gray16.png" | grep --quiet '^  Type: Grayscale$'
identify -verbose "$tempdir/gray16.png" | grep --quiet '^  Depth: 16-bit$'
identify -verbose "$tempdir/gray16.png" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/gray16.png" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/gray16.png" | grep --quiet '^    png:IHDR.bit-depth-orig: 16$'
identify -verbose "$tempdir/gray16.png" | grep --quiet '^    png:IHDR.bit_depth: 16$'
identify -verbose "$tempdir/gray16.png" | grep --quiet '^    png:IHDR.color-type-orig: 0$'
identify -verbose "$tempdir/gray16.png" | grep --quiet '^    png:IHDR.color_type: 0 (Grayscale)$'
identify -verbose "$tempdir/gray16.png" | grep --quiet '^    png:IHDR.interlace_method: 0 (Not interlaced)$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/gray16.png" "$tempdir/out.pdf"

# ghostscript outputs 8-bit grayscale, so the comparison will not be exact
gs -dQUIET -dNOPAUSE -dBATCH -sDEVICE=pnggray -r96 -sOutputFile="$tempdir/gs-%00d.png" "$tempdir/out.pdf"
similar "$tempdir/gray16.png" "$tempdir/gs-1.png"
rm "$tempdir/gs-1.png"

# poppler outputs 8-bit grayscale so the comparison will not be exact
pdftocairo -r 96 -png "$tempdir/out.pdf" "$tempdir/poppler"
similar "$tempdir/gray16.png" "$tempdir/poppler-1.png"
rm "$tempdir/poppler-1.png"

# pdfimages outputs 8-bit grayscale so the comparison will not be exact
pdfimages -png "$tempdir/out.pdf" "$tempdir/images"
similar "$tempdir/gray16.png" "$tempdir/images-000.png"
rm "$tempdir/images-000.png"

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 16
Resources.XObject.Im0.ColorSpace == "/DeviceGray"
Resources.XObject.Im0.DecodeParms.BitsPerComponent == 16
Resources.XObject.Im0.DecodeParms.Colors == 1
Resources.XObject.Im0.DecodeParms.Predictor == 15
Resources.XObject.Im0.Filter == "/FlateDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
rm "$tempdir/out.pdf"
done

j=$((j+1))

###############################################################################
for i in 1 2 4 8; do
	echo "Test $j/$tests PNG Palette$i"

	identify -verbose "$tempdir/palette$i.png" | grep --quiet '^  Format: PNG (Portable Network Graphics)$'
	identify -verbose "$tempdir/palette$i.png" | grep --quiet '^  Mime type: image/png$'
	identify -verbose "$tempdir/palette$i.png" | grep --quiet '^  Geometry: 60x60+0+0$'
	identify -verbose "$tempdir/palette$i.png" | grep --quiet '^  Colorspace: sRGB$'
	identify -verbose "$tempdir/palette$i.png" | grep --quiet '^  Type: Palette$'
	identify -verbose "$tempdir/palette$i.png" | grep --quiet '^  Depth: 8-bit$'
	identify -verbose "$tempdir/palette$i.png" | grep --quiet '^  Page geometry: 60x60+0+0$'
	identify -verbose "$tempdir/palette$i.png" | grep --quiet '^  Compression: Zip$'
	identify -verbose "$tempdir/palette$i.png" | grep --quiet "^    png:IHDR.bit-depth-orig: $i$"
	identify -verbose "$tempdir/palette$i.png" | grep --quiet "^    png:IHDR.bit_depth: $i$"
	identify -verbose "$tempdir/palette$i.png" | grep --quiet '^    png:IHDR.color-type-orig: 3$'
	identify -verbose "$tempdir/palette$i.png" | grep --quiet '^    png:IHDR.color_type: 3 (Indexed)$'
	identify -verbose "$tempdir/palette$i.png" | grep --quiet '^    png:IHDR.interlace_method: 0 (Not interlaced)$'

	for engine in $available_engines; do
	if [ $engine = "pdfrw" ]; then
		continue
	fi
	img2pdf $engine "$tempdir/palette$i.png" "$tempdir/out.pdf"

	compare_rendered "$tempdir/out.pdf" "$tempdir/palette$i.png"

	# pdfimages cannot export palette based images

	cat << END | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == $i
Resources.XObject.Im0.ColorSpace[0] == "/Indexed"
Resources.XObject.Im0.ColorSpace[1] == "/DeviceRGB"
Resources.XObject.Im0.DecodeParms.BitsPerComponent == $i
Resources.XObject.Im0.DecodeParms.Colors == 1
Resources.XObject.Im0.DecodeParms.Predictor == 15
Resources.XObject.Im0.Filter == "/FlateDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
	rm "$tempdir/out.pdf"
	done

	j=$((j+1))
done

###############################################################################
echo "Test $j/$tests GIF transparent"

convert "$tempdir/alpha.png" "$tempdir/alpha.gif"

identify -verbose "$tempdir/alpha.gif" | grep --quiet '^  Format: GIF (CompuServe graphics interchange format)$'
identify -verbose "$tempdir/alpha.gif" | grep --quiet '^  Mime type: image/gif$'
identify -verbose "$tempdir/alpha.gif" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/alpha.gif" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/alpha.gif" | grep --quiet '^  Type: PaletteAlpha$'
identify -verbose "$tempdir/alpha.gif" | grep --quiet '^  Depth: 8-bit$'
identify -verbose "$tempdir/alpha.gif" | grep --quiet '^  Colormap entries: 256$'
identify -verbose "$tempdir/alpha.gif" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/alpha.gif" | grep --quiet '^  Compression: LZW$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/alpha.gif" /dev/null && rc=$? || rc=$?
if [ "$rc" -eq 0 ]; then
	echo needs to fail here
	exit 1
fi
done

rm "$tempdir/alpha.gif"
j=$((j+1))

###############################################################################
for i in 1 2 4 8; do
	echo "Test $j/$tests GIF Palette$i"

	convert "$tempdir/palette$i.png" "$tempdir/palette$i.gif"

	identify -verbose "$tempdir/palette$i.gif" | grep --quiet '^  Format: GIF (CompuServe graphics interchange format)$'
	identify -verbose "$tempdir/palette$i.gif" | grep --quiet '^  Mime type: image/gif$'
	identify -verbose "$tempdir/palette$i.gif" | grep --quiet '^  Geometry: 60x60+0+0$'
	identify -verbose "$tempdir/palette$i.gif" | grep --quiet '^  Colorspace: sRGB$'
	identify -verbose "$tempdir/palette$i.gif" | grep --quiet '^  Type: Palette$'
	identify -verbose "$tempdir/palette$i.gif" | grep --quiet '^  Depth: 8-bit$'
	case $i in
		1) identify -verbose "$tempdir/palette$i.gif" | grep --quiet '^  Colormap entries: 2$';;
		2) identify -verbose "$tempdir/palette$i.gif" | grep --quiet '^  Colormap entries: 4$';;
		4) identify -verbose "$tempdir/palette$i.gif" | grep --quiet '^  Colormap entries: 16$';;
		8) identify -verbose "$tempdir/palette$i.gif" | grep --quiet '^  Colormap entries: 256$';;
	esac
	identify -verbose "$tempdir/palette$i.gif" | grep --quiet '^  Page geometry: 60x60+0+0$'
	identify -verbose "$tempdir/palette$i.gif" | grep --quiet '^  Compression: LZW$'

	for engine in $available_engines; do
	if [ $engine = "pdfrw" ]; then
		continue
	fi
	img2pdf $engine "$tempdir/palette$i.gif" "$tempdir/out.pdf"

	compare_rendered "$tempdir/out.pdf" "$tempdir/palette$i.png"

	# pdfimages cannot export palette based images

	cat << END | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == $i
Resources.XObject.Im0.ColorSpace[0] == "/Indexed"
Resources.XObject.Im0.ColorSpace[1] == "/DeviceRGB"
Resources.XObject.Im0.DecodeParms.BitsPerComponent == $i
Resources.XObject.Im0.DecodeParms.Colors == 1
Resources.XObject.Im0.DecodeParms.Predictor == 15
Resources.XObject.Im0.Filter == "/FlateDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
	rm "$tempdir/out.pdf"
	done

	rm "$tempdir/palette$i.gif"
	j=$((j+1))
done

###############################################################################
echo "Test $j/$tests GIF animation"

convert "$tempdir/normal.png" "$tempdir/inverse.png" -strip "$tempdir/animation.gif"

identify -verbose "$tempdir/animation.gif[0]" | grep --quiet '^  Format: GIF (CompuServe graphics interchange format)$'
identify -verbose "$tempdir/animation.gif[0]" | grep --quiet '^  Mime type: image/gif$'
identify -verbose "$tempdir/animation.gif[0]" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/animation.gif[0]" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/animation.gif[0]" | grep --quiet '^  Type: Palette$'
identify -verbose "$tempdir/animation.gif[0]" | grep --quiet '^  Depth: 8-bit$'
identify -verbose "$tempdir/animation.gif[0]" | grep --quiet '^  Colormap entries: 256$'
identify -verbose "$tempdir/animation.gif[0]" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/animation.gif[0]" | grep --quiet '^  Compression: LZW$'

identify -verbose "$tempdir/animation.gif[1]" | grep --quiet '^  Format: GIF (CompuServe graphics interchange format)$'
identify -verbose "$tempdir/animation.gif[1]" | grep --quiet '^  Mime type: image/gif$'
identify -verbose "$tempdir/animation.gif[1]" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/animation.gif[1]" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/animation.gif[1]" | grep --quiet '^  Type: Palette$'
identify -verbose "$tempdir/animation.gif[1]" | grep --quiet '^  Depth: 8-bit$'
identify -verbose "$tempdir/animation.gif[1]" | grep --quiet '^  Colormap entries: 256$'
identify -verbose "$tempdir/animation.gif[1]" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/animation.gif[1]" | grep --quiet '^  Compression: LZW$'
identify -verbose "$tempdir/animation.gif[1]" | grep --quiet '^  Scene: 1$'

for engine in $available_engines; do
if [ $engine = "pdfrw" ]; then
	continue
fi
img2pdf $engine "$tempdir/animation.gif" "$tempdir/out.pdf"

if [ "$(pdfinfo "$tempdir/out.pdf" | awk '/Pages:/ {print $2}')" != 2 ]; then
	echo "pdf does not have 2 pages"
	exit 1
fi

pdfseparate "$tempdir/out.pdf" "$tempdir/page-%d.pdf"
rm "$tempdir/out.pdf"

for page in 1 2; do
	compare_rendered "$tempdir/page-$page.pdf" "$tempdir/animation.gif[$((page-1))]"

	# pdfimages cannot export palette based images

	cat << END | checkpdf "$tempdir/page-$page.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 8
Resources.XObject.Im0.ColorSpace[0] == "/Indexed"
Resources.XObject.Im0.ColorSpace[1] == "/DeviceRGB"
Resources.XObject.Im0.DecodeParms.BitsPerComponent == 8
Resources.XObject.Im0.DecodeParms.Colors == 1
Resources.XObject.Im0.DecodeParms.Predictor == 15
Resources.XObject.Im0.Filter == "/FlateDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END

	rm "$tempdir/page-$page.pdf"
done
done

rm "$tempdir/animation.gif"
j=$((j+1))

###############################################################################
echo "Test $j/$tests TIFF float"

convert "$tempdir/normal.png" -depth 32 -define quantum:format=floating-point "$tempdir/float.tiff"

identify -verbose "$tempdir/float.tiff" | grep --quiet '^  Format: TIFF (Tagged Image File Format)$'
identify -verbose "$tempdir/float.tiff" | grep --quiet '^  Mime type: image/tiff$'
identify -verbose "$tempdir/float.tiff" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/float.tiff" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/float.tiff" | grep --quiet '^  Type: TrueColor$'
identify -verbose "$tempdir/float.tiff" | grep --quiet '^  Endiann\?ess: LSB$'
identify -verbose "$tempdir/float.tiff" | grep --quiet '^  Depth: 32/\(8\|16\)-bit$'  # imagemagick may produce a Depth: 32/8-bit or 32/16-bit image
identify -verbose "$tempdir/float.tiff" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/float.tiff" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/float.tiff" | grep --quiet '^    quantum:format: floating-point$'
identify -verbose "$tempdir/float.tiff" | grep --quiet '^    tiff:alpha: unspecified$'
identify -verbose "$tempdir/float.tiff" | grep --quiet '^    tiff:endian: lsb$'
identify -verbose "$tempdir/float.tiff" | grep --quiet '^    tiff:photometric: RGB$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/float.tiff" /dev/null && rc=$? || rc=$?
if [ "$rc" -eq 0 ]; then
	echo needs to fail here
	exit 1
fi
done

rm "$tempdir/float.tiff"
j=$((j+1))

###############################################################################
echo "Test $j/$tests TIFF CMYK8"

convert "$tempdir/normal.png" -colorspace cmyk "$tempdir/cmyk8.tiff"

identify -verbose "$tempdir/cmyk8.tiff" | grep --quiet '^  Format: TIFF (Tagged Image File Format)$'
identify -verbose "$tempdir/cmyk8.tiff" | grep --quiet '^  Mime type: image/tiff$'
identify -verbose "$tempdir/cmyk8.tiff" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/cmyk8.tiff" | grep --quiet '^  Colorspace: CMYK$'
identify -verbose "$tempdir/cmyk8.tiff" | grep --quiet '^  Type: ColorSeparation$'
identify -verbose "$tempdir/cmyk8.tiff" | grep --quiet '^  Endiann\?ess: LSB$'
identify -verbose "$tempdir/cmyk8.tiff" | grep --quiet '^  Depth: 8-bit$'
identify -verbose "$tempdir/cmyk8.tiff" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/cmyk8.tiff" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/cmyk8.tiff" | grep --quiet '^    tiff:alpha: unspecified$'
identify -verbose "$tempdir/cmyk8.tiff" | grep --quiet '^    tiff:endian: lsb$'
identify -verbose "$tempdir/cmyk8.tiff" | grep --quiet '^    tiff:photometric: separated$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/cmyk8.tiff" "$tempdir/out.pdf"

compare_ghostscript "$tempdir/out.pdf" "$tempdir/cmyk8.tiff" tiff32nc

# not testing with poppler as it cannot write CMYK images

mutool draw -o "$tempdir/mupdf.pam" -r 96 -c cmyk "$pdf" 2>/dev/null
compare -metric AE "$tempdir/cmyk8.tiff" "$tempdir/mupdf.pam" null: 2>/dev/null
rm "$tempdir/mupdf.pam"

pdfimages -tiff "$tempdir/out.pdf" "$tempdir/images"
compare -metric AE "$tempdir/cmyk8.tiff" "$tempdir/images-000.tif" null: 2>/dev/null
rm "$tempdir/images-000.tif"

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 8
Resources.XObject.Im0.ColorSpace == "/DeviceCMYK"
Resources.XObject.Im0.Filter == "/FlateDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
rm "$tempdir/out.pdf"
done

rm "$tempdir/cmyk8.tiff"
j=$((j+1))

###############################################################################
echo "Test $j/$tests TIFF CMYK16"

convert "$tempdir/normal.png" -depth 16 -colorspace cmyk "$tempdir/cmyk16.tiff"

identify -verbose "$tempdir/cmyk16.tiff" | grep --quiet '^  Format: TIFF (Tagged Image File Format)$'
identify -verbose "$tempdir/cmyk16.tiff" | grep --quiet '^  Mime type: image/tiff$'
identify -verbose "$tempdir/cmyk16.tiff" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/cmyk16.tiff" | grep --quiet '^  Colorspace: CMYK$'
identify -verbose "$tempdir/cmyk16.tiff" | grep --quiet '^  Type: ColorSeparation$'
identify -verbose "$tempdir/cmyk16.tiff" | grep --quiet '^  Endiann\?ess: LSB$'
identify -verbose "$tempdir/cmyk16.tiff" | grep --quiet '^  Depth: 16-bit$'
identify -verbose "$tempdir/cmyk16.tiff" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/cmyk16.tiff" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/cmyk16.tiff" | grep --quiet '^    tiff:alpha: unspecified$'
identify -verbose "$tempdir/cmyk16.tiff" | grep --quiet '^    tiff:endian: lsb$'
identify -verbose "$tempdir/cmyk16.tiff" | grep --quiet '^    tiff:photometric: separated$'

# PIL is unable to read 16 bit CMYK images
for engine in $available_engines; do
img2pdf $engine "$tempdir/cmyk16.gif" /dev/null && rc=$? || rc=$?
if [ "$rc" -eq 0 ]; then
	echo needs to fail here
	exit 1
fi
done

rm "$tempdir/cmyk16.tiff"
j=$((j+1))

###############################################################################
echo "Test $j/$tests TIFF RGB8"

convert "$tempdir/normal.png" "$tempdir/normal.tiff"

identify -verbose "$tempdir/normal.tiff" | grep --quiet '^  Format: TIFF (Tagged Image File Format)$'
identify -verbose "$tempdir/normal.tiff" | grep --quiet '^  Mime type: image/tiff$'
identify -verbose "$tempdir/normal.tiff" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/normal.tiff" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/normal.tiff" | grep --quiet '^  Type: TrueColor$'
identify -verbose "$tempdir/normal.tiff" | grep --quiet '^  Endiann\?ess: LSB$'
identify -verbose "$tempdir/normal.tiff" | grep --quiet '^  Depth: 8-bit$'
identify -verbose "$tempdir/normal.tiff" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/normal.tiff" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/normal.tiff" | grep --quiet '^    tiff:alpha: unspecified$'
identify -verbose "$tempdir/normal.tiff" | grep --quiet '^    tiff:endian: lsb$'
identify -verbose "$tempdir/normal.tiff" | grep --quiet '^    tiff:photometric: RGB$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/normal.tiff" "$tempdir/out.pdf"

compare_rendered "$tempdir/out.pdf" "$tempdir/normal.tiff" tiff24nc

compare_pdfimages "$tempdir/out.pdf" "$tempdir/normal.tiff"

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 8
Resources.XObject.Im0.ColorSpace == "/DeviceRGB"
Resources.XObject.Im0.DecodeParms.BitsPerComponent == 8
Resources.XObject.Im0.DecodeParms.Colors == 3
Resources.XObject.Im0.DecodeParms.Predictor == 15
Resources.XObject.Im0.Filter == "/FlateDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
rm "$tempdir/out.pdf"
done

rm "$tempdir/normal.tiff"
j=$((j+1))

###############################################################################
echo "Test $j/$tests TIFF RGBA8"

convert "$tempdir/alpha.png" -depth 8 -strip "$tempdir/alpha8.tiff"

identify -verbose "$tempdir/alpha8.tiff" | grep --quiet '^  Format: TIFF (Tagged Image File Format)$'
identify -verbose "$tempdir/alpha8.tiff" | grep --quiet '^  Mime type: image/tiff$'
identify -verbose "$tempdir/alpha8.tiff" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/alpha8.tiff" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/alpha8.tiff" | grep --quiet '^  Type: TrueColorAlpha$'
identify -verbose "$tempdir/alpha8.tiff" | grep --quiet '^  Endiann\?ess: LSB$'
identify -verbose "$tempdir/alpha8.tiff" | grep --quiet '^  Depth: 8-bit$'
identify -verbose "$tempdir/alpha8.tiff" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/alpha8.tiff" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/alpha8.tiff" | grep --quiet '^    tiff:alpha: unassociated$'
identify -verbose "$tempdir/alpha8.tiff" | grep --quiet '^    tiff:endian: lsb$'
identify -verbose "$tempdir/alpha8.tiff" | grep --quiet '^    tiff:photometric: RGB$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/alpha8.tiff" /dev/null && rc=$? || rc=$?
if [ "$rc" -eq 0 ]; then
	echo needs to fail here
	exit 1
fi
done

rm "$tempdir/alpha8.tiff"
j=$((j+1))

###############################################################################
echo "Test $j/$tests TIFF RGBA16"

convert "$tempdir/alpha.png" -strip "$tempdir/alpha16.tiff"

identify -verbose "$tempdir/alpha16.tiff" | grep --quiet '^  Format: TIFF (Tagged Image File Format)$'
identify -verbose "$tempdir/alpha16.tiff" | grep --quiet '^  Mime type: image/tiff$'
identify -verbose "$tempdir/alpha16.tiff" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/alpha16.tiff" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/alpha16.tiff" | grep --quiet '^  Type: TrueColorAlpha$'
identify -verbose "$tempdir/alpha16.tiff" | grep --quiet '^  Endiann\?ess: LSB$'
identify -verbose "$tempdir/alpha16.tiff" | grep --quiet '^  Depth: 16-bit$'
identify -verbose "$tempdir/alpha16.tiff" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/alpha16.tiff" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/alpha16.tiff" | grep --quiet '^    tiff:alpha: unassociated$'
identify -verbose "$tempdir/alpha16.tiff" | grep --quiet '^    tiff:endian: lsb$'
identify -verbose "$tempdir/alpha16.tiff" | grep --quiet '^    tiff:photometric: RGB$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/alpha16.tiff" /dev/null && rc=$? || rc=$?
if [ "$rc" -eq 0 ]; then
	echo needs to fail here
	exit 1
fi
done

rm "$tempdir/alpha16.tiff"
j=$((j+1))

###############################################################################
echo "Test $j/$tests TIFF Gray1"

convert "$tempdir/gray1.png" -depth 1 "$tempdir/gray1.tiff"

identify -verbose "$tempdir/gray1.tiff" | grep --quiet '^  Format: TIFF (Tagged Image File Format)$'
identify -verbose "$tempdir/gray1.tiff" | grep --quiet '^  Mime type: image/tiff$'
identify -verbose "$tempdir/gray1.tiff" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/gray1.tiff" | grep --quiet '^  Colorspace: Gray$'
identify -verbose "$tempdir/gray1.tiff" | grep --quiet '^  Type: Bilevel$'
identify -verbose "$tempdir/gray1.tiff" | grep --quiet '^  Endiann\?ess: LSB$'
identify -verbose "$tempdir/gray1.tiff" | grep --quiet '^  Depth: 1-bit$'
identify -verbose "$tempdir/gray1.tiff" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/gray1.tiff" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/gray1.tiff" | grep --quiet '^    tiff:alpha: unspecified$'
identify -verbose "$tempdir/gray1.tiff" | grep --quiet '^    tiff:endian: lsb$'
identify -verbose "$tempdir/gray1.tiff" | grep --quiet '^    tiff:photometric: min-is-black$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/gray1.tiff" "$tempdir/out.pdf"

compare_rendered "$tempdir/out.pdf" "$tempdir/gray1.png" pnggray

compare_pdfimages "$tempdir/out.pdf" "$tempdir/gray1.png"

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 1
Resources.XObject.Im0.ColorSpace == "/DeviceGray"
Resources.XObject.Im0.DecodeParms[0].BlackIs1 == True
Resources.XObject.Im0.DecodeParms[0].Columns == 60
Resources.XObject.Im0.DecodeParms[0].K == -1
Resources.XObject.Im0.DecodeParms[0].Rows == 60
Resources.XObject.Im0.Filter[0] == "/CCITTFaxDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
rm "$tempdir/out.pdf"
done

rm "$tempdir/gray1.tiff"
j=$((j+1))

###############################################################################
for i in 2 4 8; do
	echo "Test $j/$tests TIFF Gray$i"

	convert "$tempdir/gray$i.png" -depth $i "$tempdir/gray$i.tiff"

	identify -verbose "$tempdir/gray$i.tiff" | grep --quiet '^  Format: TIFF (Tagged Image File Format)$'
	identify -verbose "$tempdir/gray$i.tiff" | grep --quiet '^  Mime type: image/tiff$'
	identify -verbose "$tempdir/gray$i.tiff" | grep --quiet '^  Geometry: 60x60+0+0$'
	identify -verbose "$tempdir/gray$i.tiff" | grep --quiet '^  Colorspace: Gray$'
	identify -verbose "$tempdir/gray$i.tiff" | grep --quiet '^  Type: Grayscale$'
	identify -verbose "$tempdir/gray$i.tiff" | grep --quiet '^  Endiann\?ess: LSB$'
	identify -verbose "$tempdir/gray$i.tiff" | grep --quiet "^  Depth: $i-bit$"
	identify -verbose "$tempdir/gray$i.tiff" | grep --quiet '^  Page geometry: 60x60+0+0$'
	identify -verbose "$tempdir/gray$i.tiff" | grep --quiet '^  Compression: Zip$'
	identify -verbose "$tempdir/gray$i.tiff" | grep --quiet '^    tiff:alpha: unspecified$'
	identify -verbose "$tempdir/gray$i.tiff" | grep --quiet '^    tiff:endian: lsb$'
	identify -verbose "$tempdir/gray$i.tiff" | grep --quiet '^    tiff:photometric: min-is-black$'

	for engine in $available_engines; do
	img2pdf $engine "$tempdir/gray$i.tiff" "$tempdir/out.pdf"

	compare_rendered "$tempdir/out.pdf" "$tempdir/gray$i.png" pnggray

	compare_pdfimages "$tempdir/out.pdf" "$tempdir/gray$i.png"

	# When saving a PNG, PIL will store it as 8-bit data
	cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 8
Resources.XObject.Im0.ColorSpace == "/DeviceGray"
Resources.XObject.Im0.DecodeParms.BitsPerComponent == 8
Resources.XObject.Im0.DecodeParms.Colors == 1
Resources.XObject.Im0.DecodeParms.Predictor == 15
Resources.XObject.Im0.Filter == "/FlateDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
	rm "$tempdir/out.pdf"
	done

	rm "$tempdir/gray$i.tiff"
	j=$((j+1))
done

################################################################################
echo "Test $j/$tests TIFF Gray16"

convert "$tempdir/gray16.png" -depth 16 "$tempdir/gray16.tiff"

identify -verbose "$tempdir/gray16.tiff" | grep --quiet '^  Format: TIFF (Tagged Image File Format)$'
identify -verbose "$tempdir/gray16.tiff" | grep --quiet '^  Mime type: image/tiff$'
identify -verbose "$tempdir/gray16.tiff" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/gray16.tiff" | grep --quiet '^  Colorspace: Gray$'
identify -verbose "$tempdir/gray16.tiff" | grep --quiet '^  Type: Grayscale$'
identify -verbose "$tempdir/gray16.tiff" | grep --quiet '^  Endiann\?ess: LSB$'
identify -verbose "$tempdir/gray16.tiff" | grep --quiet "^  Depth: 16-bit$"
identify -verbose "$tempdir/gray16.tiff" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/gray16.tiff" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/gray16.tiff" | grep --quiet '^    tiff:alpha: unspecified$'
identify -verbose "$tempdir/gray16.tiff" | grep --quiet '^    tiff:endian: lsb$'
identify -verbose "$tempdir/gray16.tiff" | grep --quiet '^    tiff:photometric: min-is-black$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/gray16.tiff" /dev/null && rc=$? || rc=$?
if [ "$rc" -eq 0 ]; then
	echo needs to fail here
	exit 1
fi
done

rm "$tempdir/gray16.tiff"
j=$((j+1))

###############################################################################
echo "Test $j/$tests TIFF multipage"

convert "$tempdir/normal.png" "$tempdir/inverse.png" -strip "$tempdir/multipage.tiff"

identify -verbose "$tempdir/multipage.tiff[0]" | grep --quiet '^  Format: TIFF (Tagged Image File Format)$'
identify -verbose "$tempdir/multipage.tiff[0]" | grep --quiet '^  Mime type: image/tiff$'
identify -verbose "$tempdir/multipage.tiff[0]" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/multipage.tiff[0]" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/multipage.tiff[0]" | grep --quiet '^  Type: TrueColor$'
identify -verbose "$tempdir/multipage.tiff[0]" | grep --quiet '^  Endiann\?ess: LSB$'
identify -verbose "$tempdir/multipage.tiff[0]" | grep --quiet '^  Depth: 8-bit$'
identify -verbose "$tempdir/multipage.tiff[0]" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/multipage.tiff[0]" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/multipage.tiff[0]" | grep --quiet '^    tiff:alpha: unspecified$'
identify -verbose "$tempdir/multipage.tiff[0]" | grep --quiet '^    tiff:endian: lsb$'
identify -verbose "$tempdir/multipage.tiff[0]" | grep --quiet '^    tiff:photometric: RGB$'

identify -verbose "$tempdir/multipage.tiff[1]" | grep --quiet '^  Format: TIFF (Tagged Image File Format)$'
identify -verbose "$tempdir/multipage.tiff[1]" | grep --quiet '^  Mime type: image/tiff$'
identify -verbose "$tempdir/multipage.tiff[1]" | grep --quiet '^  Geometry: 60x60+0+0$'
identify -verbose "$tempdir/multipage.tiff[1]" | grep --quiet '^  Colorspace: sRGB$'
identify -verbose "$tempdir/multipage.tiff[1]" | grep --quiet '^  Type: TrueColor$'
identify -verbose "$tempdir/multipage.tiff[1]" | grep --quiet '^  Endiann\?ess: LSB$'
identify -verbose "$tempdir/multipage.tiff[1]" | grep --quiet '^  Depth: 8-bit$'
identify -verbose "$tempdir/multipage.tiff[1]" | grep --quiet '^  Page geometry: 60x60+0+0$'
identify -verbose "$tempdir/multipage.tiff[1]" | grep --quiet '^  Compression: Zip$'
identify -verbose "$tempdir/multipage.tiff[1]" | grep --quiet '^    tiff:alpha: unspecified$'
identify -verbose "$tempdir/multipage.tiff[1]" | grep --quiet '^    tiff:endian: lsb$'
identify -verbose "$tempdir/multipage.tiff[1]" | grep --quiet '^    tiff:photometric: RGB$'
identify -verbose "$tempdir/multipage.tiff[1]" | grep --quiet '^  Scene: 1$'

for engine in $available_engines; do
img2pdf $engine "$tempdir/multipage.tiff" "$tempdir/out.pdf"

if [ "$(pdfinfo "$tempdir/out.pdf" | awk '/Pages:/ {print $2}')" != 2 ]; then
	echo "pdf does not have 2 pages"
	exit 1
fi

pdfseparate "$tempdir/out.pdf" "$tempdir/page-%d.pdf"
rm "$tempdir/out.pdf"

for page in 1 2; do
	compare_rendered "$tempdir/page-$page.pdf" "$tempdir/multipage.tiff[$((page-1))]"

	compare_pdfimages "$tempdir/page-$page.pdf" "$tempdir/multipage.tiff[$((page-1))]"

	cat << 'END' | checkpdf "$tempdir/page-$page.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 8
Resources.XObject.Im0.ColorSpace == "/DeviceRGB"
Resources.XObject.Im0.DecodeParms.BitsPerComponent == 8
Resources.XObject.Im0.DecodeParms.Colors == 3
Resources.XObject.Im0.DecodeParms.Predictor == 15
Resources.XObject.Im0.Filter == "/FlateDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END

	rm "$tempdir/page-$page.pdf"
done
done

rm "$tempdir/multipage.tiff"
j=$((j+1))

###############################################################################
for i in 1 2 4 8; do
	echo "Test $j/$tests TIFF Palette$i"

	convert "$tempdir/palette$i.png" "$tempdir/palette$i.tiff"

	identify -verbose "$tempdir/palette$i.tiff" | grep --quiet '^  Format: TIFF (Tagged Image File Format)$'
	identify -verbose "$tempdir/palette$i.tiff" | grep --quiet '^  Mime type: image/tiff$'
	identify -verbose "$tempdir/palette$i.tiff" | grep --quiet '^  Geometry: 60x60+0+0$'
	identify -verbose "$tempdir/palette$i.tiff" | grep --quiet '^  Colorspace: sRGB$'
	identify -verbose "$tempdir/palette$i.tiff" | grep --quiet '^  Type: Palette$'
	identify -verbose "$tempdir/palette$i.tiff" | grep --quiet '^  Endiann\?ess: LSB$'
	if [ "$i" -eq 8 ]; then
		identify -verbose "$tempdir/palette$i.tiff" | grep --quiet "^  Depth: 8-bit$"
	else
		identify -verbose "$tempdir/palette$i.tiff" | grep --quiet "^  Depth: $i/8-bit$"
	fi
	case $i in
		1) identify -verbose "$tempdir/palette$i.tiff" | grep --quiet '^  Colormap entries: 2$';;
		2) identify -verbose "$tempdir/palette$i.tiff" | grep --quiet '^  Colormap entries: 4$';;
		4) identify -verbose "$tempdir/palette$i.tiff" | grep --quiet '^  Colormap entries: 16$';;
		8) identify -verbose "$tempdir/palette$i.tiff" | grep --quiet '^  Colormap entries: 256$';;
	esac
	identify -verbose "$tempdir/palette$i.tiff" | grep --quiet '^  Page geometry: 60x60+0+0$'
	identify -verbose "$tempdir/palette$i.tiff" | grep --quiet '^  Compression: Zip$'
	identify -verbose "$tempdir/palette$i.tiff" | grep --quiet '^    tiff:alpha: unspecified$'
	identify -verbose "$tempdir/palette$i.tiff" | grep --quiet '^    tiff:endian: lsb$'
	identify -verbose "$tempdir/palette$i.tiff" | grep --quiet '^    tiff:photometric: palette$'

	for engine in $available_engines; do
	if [ $engine = "pdfrw" ]; then
		continue
	fi
	img2pdf $engine "$tempdir/palette$i.tiff" "$tempdir/out.pdf"

	compare_rendered "$tempdir/out.pdf" "$tempdir/palette$i.png"

	# pdfimages cannot export palette based images

	cat << END | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == $i
Resources.XObject.Im0.ColorSpace[0] == "/Indexed"
Resources.XObject.Im0.ColorSpace[1] == "/DeviceRGB"
Resources.XObject.Im0.DecodeParms.BitsPerComponent == $i
Resources.XObject.Im0.DecodeParms.Colors == 1
Resources.XObject.Im0.DecodeParms.Predictor == 15
Resources.XObject.Im0.Filter == "/FlateDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END

	rm "$tempdir/out.pdf"
	done

	rm "$tempdir/palette$i.tiff"
	j=$((j+1))
done

###############################################################################
for i in 12 14 16; do
	echo "Test $j/$tests TIFF RGB$i"

	convert "$tempdir/normal16.png" -depth "$i" "$tempdir/normal$i.tiff"

	identify -verbose "$tempdir/normal$i.tiff" | grep --quiet '^  Format: TIFF (Tagged Image File Format)$'
	identify -verbose "$tempdir/normal$i.tiff" | grep --quiet '^  Mime type: image/tiff$'
	identify -verbose "$tempdir/normal$i.tiff" | grep --quiet '^  Geometry: 60x60+0+0$'
	identify -verbose "$tempdir/normal$i.tiff" | grep --quiet '^  Colorspace: sRGB$'
	identify -verbose "$tempdir/normal$i.tiff" | grep --quiet '^  Type: TrueColor$'
	identify -verbose "$tempdir/normal$i.tiff" | grep --quiet '^  Endiann\?ess: LSB$'
	if [ $i -eq 16 ]; then
		identify -verbose "$tempdir/normal$i.tiff" | grep --quiet "^  Depth: $i-bit$"
	else
		identify -verbose "$tempdir/normal$i.tiff" | egrep --quiet "^  Depth: $i(/16)?-bit$"
	fi
	identify -verbose "$tempdir/normal$i.tiff" | grep --quiet '^  Page geometry: 60x60+0+0$'
	identify -verbose "$tempdir/normal$i.tiff" | grep --quiet '^  Compression: Zip$'
	identify -verbose "$tempdir/normal$i.tiff" | grep --quiet '^    tiff:alpha: unspecified$'
	identify -verbose "$tempdir/normal$i.tiff" | grep --quiet '^    tiff:endian: lsb$'
	identify -verbose "$tempdir/normal$i.tiff" | grep --quiet '^    tiff:photometric: RGB$'

	for engine in $available_engines; do
	img2pdf $engine "$tempdir/normal$i.tiff" /dev/null && rc=$? || rc=$?
	if [ "$rc" -eq 0 ]; then
		echo needs to fail here
		exit 1
	fi
	done

	rm "$tempdir/normal$i.tiff"
	j=$((j+1))
done

###############################################################################
echo "Test $j/$tests TIFF CCITT Group4, little endian, msb-to-lsb, min-is-white"

convert "$tempdir/gray1.png" -compress group4 -define tiff:endian=lsb -define tiff:fill-order=msb -define quantum:polarity=min-is-white "$tempdir/group4.tiff"
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Bits/Sample: 1'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Compression Scheme: CCITT Group 4'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Photometric Interpretation: min-is-white'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'FillOrder: msb-to-lsb'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Samples/Pixel: 1'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Type: Bilevel'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Endian*ess: LSB'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Depth: 1-bit'
identify -verbose "$tempdir/group4.tiff" | grep --quiet '[gG]ray: 1-bit'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Compression: Group4'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'tiff:endian: lsb'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'tiff:photometric: min-is-white'

for engine in $available_engines; do
img2pdf $engine "$tempdir/group4.tiff" "$tempdir/out.pdf"

compare_rendered "$tempdir/out.pdf" "$tempdir/group4.tiff" pnggray

compare_pdfimages "$tempdir/out.pdf" "$tempdir/group4.tiff"

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 1
Resources.XObject.Im0.ColorSpace == "/DeviceGray"
Resources.XObject.Im0.DecodeParms[0].BlackIs1 == False
Resources.XObject.Im0.DecodeParms[0].Columns == 60
Resources.XObject.Im0.DecodeParms[0].K == -1
Resources.XObject.Im0.DecodeParms[0].Rows == 60
Resources.XObject.Im0.Filter[0] == "/CCITTFaxDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
rm "$tempdir/out.pdf"
done

rm "$tempdir/group4.tiff"
j=$((j+1))

###############################################################################
echo "Test $j/$tests TIFF CCITT Group4, big endian, msb-to-lsb, min-is-white"

convert "$tempdir/gray1.png" -compress group4 -define tiff:endian=msb -define tiff:fill-order=msb -define quantum:polarity=min-is-white "$tempdir/group4.tiff"
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Bits/Sample: 1'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Compression Scheme: CCITT Group 4'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Photometric Interpretation: min-is-white'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'FillOrder: msb-to-lsb'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Samples/Pixel: 1'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Type: Bilevel'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Endian*ess: MSB'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Depth: 1-bit'
identify -verbose "$tempdir/group4.tiff" | grep --quiet '[gG]ray: 1-bit'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Compression: Group4'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'tiff:endian: msb'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'tiff:photometric: min-is-white'

for engine in $available_engines; do
img2pdf $engine "$tempdir/group4.tiff" "$tempdir/out.pdf"

compare_rendered "$tempdir/out.pdf" "$tempdir/group4.tiff" pnggray

compare_pdfimages "$tempdir/out.pdf" "$tempdir/group4.tiff"

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 1
Resources.XObject.Im0.ColorSpace == "/DeviceGray"
Resources.XObject.Im0.DecodeParms[0].BlackIs1 == False
Resources.XObject.Im0.DecodeParms[0].Columns == 60
Resources.XObject.Im0.DecodeParms[0].K == -1
Resources.XObject.Im0.DecodeParms[0].Rows == 60
Resources.XObject.Im0.Filter[0] == "/CCITTFaxDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
rm "$tempdir/out.pdf"
done

rm "$tempdir/group4.tiff"
j=$((j+1))

###############################################################################
echo "Test $j/$tests TIFF CCITT Group4, big endian, lsb-to-msb, min-is-white"

convert "$tempdir/gray1.png" -compress group4 -define tiff:endian=msb -define tiff:fill-order=lsb -define quantum:polarity=min-is-white "$tempdir/group4.tiff"
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Bits/Sample: 1'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Compression Scheme: CCITT Group 4'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Photometric Interpretation: min-is-white'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'FillOrder: lsb-to-msb'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Samples/Pixel: 1'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Type: Bilevel'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Endian*ess: MSB'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Depth: 1-bit'
identify -verbose "$tempdir/group4.tiff" | grep --quiet '[gG]ray: 1-bit'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Compression: Group4'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'tiff:endian: msb'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'tiff:photometric: min-is-white'

for engine in $available_engines; do
img2pdf $engine "$tempdir/group4.tiff" "$tempdir/out.pdf"

compare_rendered "$tempdir/out.pdf" "$tempdir/group4.tiff" pnggray

compare_pdfimages "$tempdir/out.pdf" "$tempdir/group4.tiff"

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 1
Resources.XObject.Im0.ColorSpace == "/DeviceGray"
Resources.XObject.Im0.DecodeParms[0].BlackIs1 == False
Resources.XObject.Im0.DecodeParms[0].Columns == 60
Resources.XObject.Im0.DecodeParms[0].K == -1
Resources.XObject.Im0.DecodeParms[0].Rows == 60
Resources.XObject.Im0.Filter[0] == "/CCITTFaxDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
rm "$tempdir/out.pdf"
done

rm "$tempdir/group4.tiff"
j=$((j+1))

###############################################################################
echo "Test $j/$tests TIFF CCITT Group4, little endian, msb-to-lsb, min-is-black"

# We create a min-is-black group4 tiff with PIL because it creates these by
# default (and without the option to do otherwise) whereas imagemagick only
# became able to do it through commit 00730551f0a34328685c59d0dde87dd9e366103a
# See https://www.imagemagick.org/discourse-server/viewtopic.php?f=1&t=34605
python3 -c 'from PIL import Image;Image.open("'"$tempdir/gray1.png"'").save("'"$tempdir/group4.tiff"'",format="TIFF",compression="group4")'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Bits/Sample: 1'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Compression Scheme: CCITT Group 4'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Photometric Interpretation: min-is-black'
# PIL doesn't set those
#tiffinfo "$tempdir/group4.tiff" | grep --quiet 'FillOrder: msb-to-lsb'
#tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Samples/Pixel: 1'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Type: Bilevel'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Endian*ess: LSB'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Depth: 1-bit'
identify -verbose "$tempdir/group4.tiff" | grep --quiet '[gG]ray: 1-bit'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Compression: Group4'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'tiff:endian: lsb'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'tiff:photometric: min-is-black'

for engine in $available_engines; do
img2pdf $engine "$tempdir/group4.tiff" "$tempdir/out.pdf"

compare_rendered "$tempdir/out.pdf" "$tempdir/group4.tiff" pnggray

compare_pdfimages "$tempdir/out.pdf" "$tempdir/group4.tiff"

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 1
Resources.XObject.Im0.ColorSpace == "/DeviceGray"
Resources.XObject.Im0.DecodeParms[0].BlackIs1 == True
Resources.XObject.Im0.DecodeParms[0].Columns == 60
Resources.XObject.Im0.DecodeParms[0].K == -1
Resources.XObject.Im0.DecodeParms[0].Rows == 60
Resources.XObject.Im0.Filter[0] == "/CCITTFaxDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
rm "$tempdir/out.pdf"
done

rm "$tempdir/group4.tiff"
j=$((j+1))

###############################################################################
echo "Test $j/$tests TIFF CCITT Group4, without fillorder, samples/pixel, bits/sample"

convert "$tempdir/gray1.png" -compress group4 -define tiff:endian=lsb -define tiff:fill-order=msb -define quantum:polarity=min-is-white "$tempdir/group4.tiff"
# remove BitsPerSample (258)
tiffset -u 258 "$tempdir/group4.tiff"
# remove FillOrder (266)
tiffset -u 266 "$tempdir/group4.tiff"
# remove SamplesPerPixel (277)
tiffset -u 277 "$tempdir/group4.tiff"
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Bits/Sample: 1' && exit 1
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Compression Scheme: CCITT Group 4'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Photometric Interpretation: min-is-white'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'FillOrder: msb-to-lsb' && exit 1
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Samples/Pixel: 1' && exit 1
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Type: Bilevel'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Endian*ess: LSB'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Depth: 1-bit'
identify -verbose "$tempdir/group4.tiff" | grep --quiet '[gG]ray: 1-bit'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Compression: Group4'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'tiff:endian: lsb'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'tiff:photometric: min-is-white'

for engine in $available_engines; do
img2pdf $engine "$tempdir/group4.tiff" "$tempdir/out.pdf"

compare_rendered "$tempdir/out.pdf" "$tempdir/group4.tiff" pnggray

compare_pdfimages "$tempdir/out.pdf" "$tempdir/group4.tiff"

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 1
Resources.XObject.Im0.ColorSpace == "/DeviceGray"
Resources.XObject.Im0.DecodeParms[0].BlackIs1 == False
Resources.XObject.Im0.DecodeParms[0].Columns == 60
Resources.XObject.Im0.DecodeParms[0].K == -1
Resources.XObject.Im0.DecodeParms[0].Rows == 60
Resources.XObject.Im0.Filter[0] == "/CCITTFaxDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
rm "$tempdir/out.pdf"
done

rm "$tempdir/group4.tiff"
j=$((j+1))

###############################################################################
echo "Test $j/$tests TIFF CCITT Group4, without rows-per-strip"

convert "$tempdir/gray1.png" -compress group4 -define tiff:endian=lsb -define tiff:fill-order=msb -define quantum:polarity=min-is-white -define tiff:rows-per-strip=4294967295 "$tempdir/group4.tiff"
# remove RowsPerStrip (278)
tiffset -u 278 "$tempdir/group4.tiff"
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Bits/Sample: 1'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Compression Scheme: CCITT Group 4'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Photometric Interpretation: min-is-white'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'FillOrder: msb-to-lsb'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Samples/Pixel: 1'
tiffinfo "$tempdir/group4.tiff" | grep --quiet 'Rows/Strip:' && exit 1
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Type: Bilevel'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Endian*ess: LSB'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Depth: 1-bit'
identify -verbose "$tempdir/group4.tiff" | grep --quiet '[gG]ray: 1-bit'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'Compression: Group4'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'tiff:endian: lsb'
identify -verbose "$tempdir/group4.tiff" | grep --quiet 'tiff:photometric: min-is-white'

for engine in $available_engines; do
img2pdf $engine "$tempdir/group4.tiff" "$tempdir/out.pdf"

compare_rendered "$tempdir/out.pdf" "$tempdir/group4.tiff" pnggray

compare_pdfimages "$tempdir/out.pdf" "$tempdir/group4.tiff"

cat << 'END' | checkpdf "$tempdir/out.pdf"
Contents.read_bytes() == b'q\n45.0000 0 0 45.0000 0.0000 0.0000 cm\n/Im0 Do\nQ'
Resources.XObject.Im0.BitsPerComponent == 1
Resources.XObject.Im0.ColorSpace == "/DeviceGray"
Resources.XObject.Im0.DecodeParms[0].BlackIs1 == False
Resources.XObject.Im0.DecodeParms[0].Columns == 60
Resources.XObject.Im0.DecodeParms[0].K == -1
Resources.XObject.Im0.DecodeParms[0].Rows == 60
Resources.XObject.Im0.Filter[0] == "/CCITTFaxDecode"
Resources.XObject.Im0.Height == 60
Resources.XObject.Im0.Width == 60
END
rm "$tempdir/out.pdf"
done

rm "$tempdir/group4.tiff"
j=$((j+1))

rm "$tempdir/alpha.png" "$tempdir/normal.png" "$tempdir/inverse.png" "$tempdir/palette1.png" "$tempdir/palette2.png" "$tempdir/palette4.png" "$tempdir/palette8.png" "$tempdir/gray8.png" "$tempdir/normal16.png" "$tempdir/gray16.png" "$tempdir/gray4.png" "$tempdir/gray2.png" "$tempdir/gray1.png"
rmdir "$tempdir"

trap - EXIT
