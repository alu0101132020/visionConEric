// var img = new Image();

// var canvas = document.getElementById('canvas');
// var ctx = canvas.getContext('2d');
// img.crossOrigin = "Anonymous";

// img.onload = function() {
// 	ctx.putImageData(img, 0, 0);
// };


// var original = function() {
//     console.log("hola")
// 	ctx.putImageData(img, 0, 0);
// };

// var invert = function() {
//     console.log("hola")
// 	ctx.putImageData(img, 0, 0);
// 	const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
// 	const data = imageData.data;
// 	for (var i = 0; i < data.length; i += 4) {
// 		data[i]     = 255 - data[i];     // red
// 		data[i + 1] = 255 - data[i + 1]; // green
// 		data[i + 2] = 255 - data[i + 2]; // blue
// 	}
// 	ctx.putImageData(imageData, 0, 0);
// };

// var grayscale = function() {
//     console.log("hola")
// 	ctx.drawImage(img, 0, 0);
// 	const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
// 	for (var i = 0; i < imageData.data.length; i += 4) {
// 		var avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
// 		data[i]     = avg; // red
// 		data[i + 1] = avg; // green
// 		data[i + 2] = avg; // blue
// 	}
// 	ctx.putImageData(imageData, 0, 0);
// };

// const inputs = document.querySelectorAll('[name=color]');

// for (const input of inputs) {
// 	input.addEventListener("change", function(evt) {
// 		switch (evt.target.value) {
// 			case "inverted":
// 				return invert();
// 			case "grayscale":
// 				return grayscale();
// 			default:
// 				return original();
// 		}
// 	});
// }

// original();
// img.src = './assets/arbol.jpg';
//  ---------
// let cnv = document.getElementById('canvas');
// let cnx = cnv.getContext('2d');

// function grey(input) {
// 	cnx.drawImage(myimage, 0 , 0);
// 	let width = input.width;
// 	let height = input.height;
// 	let imgPixels = cnx.getImageData(0, 0, width, height);

// 	for(let y = 0; y < height; y++){
// 		for(let x = 0; x < width; x++){
// 			let i = (y * 4) * width + x * 4;
// 			let avg = (imgPixels.data[i] + imgPixels.data[i + 1] + imgPixels.data[i + 2]) / 3;
// 			imgPixels.data[i] = avg;
// 			imgPixels.data[i + 1] = avg;
// 			imgPixels.data[i + 2] = avg;
// 		}
// 	}

// 	cnx.putImageData(imgPixels, 0, 0, 0, 0, imgPixels.width, imgPixels.height);
// }

// let myimage = new Image();
// myimage.onload = function() {
// 	grey(myimage);
// }
// myimage.crossOrigin = "Anonymous";
// myimage.src = "./assets/arbol.jpg";

var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
let image = new Image();
image.src = "./assets/arbol.jpg";

image.onload = function() {
	ctx.drawImage(image, 33, 71, 104, 124, 21, 20, 87, 104);
	let width = image.width;
	let height = image.height;
	// let imgPixels = ctx.getImageData(0, 0, width, height);

	for(let y = 0; y < height; y++){
		for(let x = 0; x < width; x++){
			let i = (y * 4) * width + x * 4;
			let avg = (image.data[i] + image.image[i + 1] + image.image[i + 2]) / 3;
			image.image[i] = avg;
			image.image[i + 1] = avg;
			image.image[i + 2] = avg;
		}
	}
};

