from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.ARB.texture_cube_map import *
import numpy
from PIL import Image as Image
import sys

angle    = 0.1
texture  = 0
# glTexGeni mode
mode = GL_NORMAL_MAP_ARB

# this loads a cube map from six images
def loadCubemap ( faces, path = ""  ):
    texture = glGenTextures ( 1 )
    target_map  = GL_TEXTURE_CUBE_MAP_POSITIVE_X_ARB
    glBindTexture     ( GL_TEXTURE_CUBE_MAP_ARB, texture )
    glPixelStorei     ( GL_PACK_ALIGNMENT,1 )
    glTexParameteri   ( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,     GL_REPEAT )
    glTexParameteri   ( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,     GL_REPEAT )
    glTexParameteri   ( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
    glTexParameteri   ( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
    glEnable          ( GL_TEXTURE_CUBE_MAP_ARB )

    for face in faces:
        if path != "":
            file = path + "/" + face
        else:
            file = face
        image  = Image.open ( file )
        width  = image.size [0]
        height = image.size [1]
        image  = image.tobytes()
        gluBuild2DMipmaps ( target_map, 3, width, height, GL_RGBA, GL_UNSIGNED_BYTE, image )
        target_map = target_map + 1
    return texture

#this will check if the OpenGL ARB extension is working
def extensionInit ():
    if not glInitTextureCubeMapARB ():
        print("ARB_texture_cubemap not working !")
        sys.exit ( 1 )

def init ():

    glClearColor(0, 0, 0, 1)
    glClearDepth ( 1.0 )
    glDepthFunc  ( GL_LEQUAL )
    glEnable     ( GL_DEPTH_TEST )
    glHint       ( GL_POLYGON_SMOOTH_HINT,         GL_NICEST )
    glHint       ( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )

#this will help when resizing the window
def reshape ( width, height ):
    glViewport     ( 0, 0, width, height )
    glMatrixMode   ( GL_PROJECTION )
    glLoadIdentity ()
    gluPerspective ( 55.0, float(width)/float (height), 1.0, 60.0 )
    glMatrixMode   ( GL_MODELVIEW )
    glLoadIdentity ()
    gluLookAt      ( 0.0, 6.0, 0.0,
                     4.0, -4.0, 4.0,
                     0.0, 0.5, 0.0 )

def display ():
    global texture, mode

    glClear   ( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glEnable  ( GL_TEXTURE_CUBE_MAP_ARB )
    glEnable  ( GL_TEXTURE_GEN_S )
    glEnable  ( GL_TEXTURE_GEN_T )
    glEnable  ( GL_TEXTURE_GEN_R )
    glTexGeni ( GL_S, GL_TEXTURE_GEN_MODE, mode )
    glTexGeni ( GL_T, GL_TEXTURE_GEN_MODE, mode )
    glTexGeni ( GL_R, GL_TEXTURE_GEN_MODE, mode )

    glBindTexture   ( GL_TEXTURE_CUBE_MAP_ARB, texture )
    glPushMatrix    ()
    glTranslatef    ( 2, 2, 2 )
    glRotate       ( angle,  0, 10, 0 )
    glRotate       ( angle,  10, 0 , 0 )

    glutSolidSphere(1.5, 10, 10)

    glPopMatrix     ()
    glutSwapBuffers ()

# keyboard bindings
def keyPressed ( *args ):
    key = args [0]
    if key == '\033' or key == b'\x1b':
        sys.exit ()

# rotation
def animate ():
    global angle
    angle  = 0.01 * glutGet ( GLUT_ELAPSED_TIME )
    glutPostRedisplay ()

# main function
def main ():
    global texture

    glutInit               ( sys.argv )
    glutInitDisplayMode    ( GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH )
    glutInitWindowSize     ( 600, 400 )
    glutInitWindowPosition ( 0, 0 )

    glutCreateWindow ( "Render the Earth" )
    glutDisplayFunc  ( display )
    glutIdleFunc     ( animate )
    glutReshapeFunc  ( reshape )
    glutKeyboardFunc ( keyPressed )

    init          ()
    extensionInit ()

    texture = loadCubemap ( ( "east1.png",
                              "west.png",
                              "north.png",
                              "south.png",
                              "center.png",
                              "east2.png" ), "cubemap" )
    glutMainLoop()

if __name__ == "__main__":
  print("Hit ESC key to quit.")
  main()