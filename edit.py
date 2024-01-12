from PIL import Image
import numpy as np
size = (1920,1080)
filename = "source_img/rock.png"
filename2 = "source_img/hendrix.png"
outfile = "output_images/hendrock.png"


class Picture:
	def __init__(self,  filename, create=False, size=(0,0), filetype='PNG'):
		self.filetype = filetype
		self.filename = filename
		if create :
			self.image = Image.new('RGBA', (size) , (0,0,0,0))
			self.size = size
		else :
			self.image = Image.open(self.filename).convert('RGBA')
			self.size = self.image.size
		self.pixels = self.image.load()
		self.w = self.size[0]
		self.h = self.size[1]
		self.r = None
		self.g = None
		self.b = None
		self.a = None
		self.init_colour_arrays()

	def show(self):
		self.set_pixels()
		self.image.show()

	def save(self, filename, filetype = 'PNG'):
		self.set_pixels()
		self.image.save(filename, filetype)

	def set_alpha(self, alpha):
		for i in range(self.w) :
			for j in range(self.h) :
				pixel = list(self.pixels[i,j])
				pixel[-1] = round(alpha * 255)
				self.pixels[i,j] = tuple(pixel)

	def init_colour_arrays(self):
		self.r = np.zeros(self.size)
		self.g = np.zeros(self.size)
		self.b = np.zeros(self.size)
		self.a = np.zeros(self.size)
		for i in range(self.w) :
			for j in range(self.h) :
				self.r[i,j] = float(self.pixels[i,j][0])/255.
				self.g[i,j] = float(self.pixels[i,j][1])/255.
				self.b[i,j] = float(self.pixels[i,j][2])/255.
				self.a[i,j] = float(self.pixels[i,j][3])/255.

	def invert(self):
		self.r,self.g,self.b = 1.-self.r,1.-self.g,1.-self.b

	def make_grey(self):
		self.r,self.g,self.b = (self.r+self.g+self.b)/3.,self.r,self.r

	def make_red(self):
		self.r,self.g,self.b = self.r,0,0

	def make_green(self):
		self.r,self.g,self.b = 0,self.g,0

	def make_blue(self):
		self.r,self.g,self.b = 0,self.b,0

	def brightness_mult(self, frac):
		self.r,self.g,self.b = self.r*frac,self.g*frac,self.b*frac

	def colour_rotation(self):
		self.r,self.g,self.b = self.g,self.b,self.r

	def set_pixels(self):
		for i in range(self.w) :
			for j in range(self.h) :
				pixel = [self.r[i,j],self.g[i,j],self.b[i,j],self.a[i,j]]
				pixel = [round(255. * x) for x in pixel]
				self.pixels[i,j] = tuple(pixel)

	def recast_from_percent(self,target,x0,x1,y0,y1):
		for i in range(self.w) :
			for j in range(self.h) :
				xtilde = (x0 + (x1-x0)*float(i)/float(self.w-1) )*target.w
				ytilde = (y0 + (y1-y0)*float(j)/float(self.h-1) )*target.h
				x = int(round(xtilde))
				y = int(round(ytilde))
				dx = xtilde - round(xtilde)
				dy = ytilde - round(ytilde)
				if (x >= 0 and y>=0 and y<target.h-1 and x<target.w-1) :
					self.r[i,j] = (1-dx-dy)*target.r[x,y] + dx*target.r[x+1,y] + dy*target.r[x,y+1]
					self.b[i,j] = (1-dx-dy)*target.b[x,y] + dx*target.b[x+1,y] + dy*target.b[x,y+1]
					self.g[i,j] = (1-dx-dy)*target.g[x,y] + dx*target.g[x+1,y] + dy*target.g[x,y+1]
					self.a[i,j] = (1-dx-dy)*target.a[x,y] + dx*target.a[x+1,y] + dy*target.a[x,y+1]
				else :
					self.r[i,j] = 0.
					self.g[i,j] = 0.
					self.b[i,j] = 0.
					self.a[i,j] = 0.

	def recast_from_pixel(self,target,x0,x1,y0,y1):
		for i in range(self.w) :
			for j in range(self.h) :
				xtilde = x0 + (x1-x0)*float(i)/float(self.w-1) 
				ytilde = y0 + (y1-y0)*float(j)/float(self.h-1) 
				x = int(round(xtilde))
				y = int(round(ytilde))
				dx = xtilde - round(xtilde)
				dy = ytilde - round(ytilde)
				if (x >= 0 and y>=0 and y<target.h-1 and x<target.w-1) :
					self.r[i,j] = (1-dx-dy)*target.r[x,y] + dx*target.r[x+1,y] + dy*target.r[x,y+1]
					self.b[i,j] = (1-dx-dy)*target.b[x,y] + dx*target.b[x+1,y] + dy*target.b[x,y+1]
					self.g[i,j] = (1-dx-dy)*target.g[x,y] + dx*target.g[x+1,y] + dy*target.g[x,y+1]
					self.a[i,j] = (1-dx-dy)*target.a[x,y] + dx*target.a[x+1,y] + dy*target.a[x,y+1]
				else :
					self.r[i,j] = 0.
					self.g[i,j] = 0.
					self.b[i,j] = 0.
					self.a[i,j] = 0.

	def blend(self,target1,target2,blend1, blend2):
		for i in range(self.w) :
			for j in range(self.h) :
				self.r[i,j] = target1.r[i,j] * blend1 + (target2.r[i,j]-0.5) * blend2 
				self.g[i,j] = target1.g[i,j] * blend1 + (target2.g[i,j]-0.5) * blend2
				self.b[i,j] = target1.b[i,j] * blend1 + (target2.b[i,j]-0.5) * blend2
				self.a[i,j] = target1.a[i,j] * blend1 + (target2.a[i,j]-0.5) * blend2



rock = Picture('source_img/rock.png')
rock.show()

lizard = Picture('source_img/lizard.png')
lizard.show()

squarerock = Picture('output_images/square_rock.png',True,(1024,1024))
squarerock.recast_from_pixel(rock,10,700,10,700)
squarerock.brightness_mult(0.7)
squarerock.show()

hendrock = Picture(outfile, True, (1024,1024))
hendrock.blend(lizard,squarerock,1.,2.0)
hendrock.show()
hendrock.save("ouput_images/hendrock.png")

# mix = Image.new('RGBA', (768,1024) , (0,0,0,0))
# mix.paste(hendrock.image, (0,0) )
# mix.paste(rock.image, (0,0) )
# mix.show()

# im.save(outfile, "PNG")



# resize
# colour mapping func
# safeguard from colour overdrive over 1.0 or 255
# code up stats like average colours and deviations to help with mixes and amsks
# code up compression or a sigmoid function
