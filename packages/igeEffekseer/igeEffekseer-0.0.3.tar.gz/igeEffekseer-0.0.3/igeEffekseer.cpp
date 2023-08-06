#include "igeEffekseer.h"
#include "igeEffekseer_doc_en.h"

static PyObject* onTextureLoaderCallBack = nullptr;

float* pyObjToFloat(PyObject* obj, float* f, int& d) {
	if (f) {
		f[0] = f[1] = f[2] = 0.0f;
	}

	if (obj)
	{
		if (PyTuple_Check(obj)) {
			d = (int)PyTuple_Size(obj);
			if (d > 3) d = 3;
			for (int j = 0; j < d; j++) {
				PyObject* val = PyTuple_GET_ITEM(obj, j);
				f[j] = (float)PyFloat_AsDouble(val);
			}
		}
		else if (PyList_Check(obj)) {
			d = (int)PyList_Size(obj);
			if (d > 3) d = 3;
			for (int j = 0; j < d; j++) {
				PyObject* val = PyList_GET_ITEM(obj, j);
				f[j] = (float)PyFloat_AsDouble(val);
			}
		}
	}
	return f;
}

Effekseer::TextureData* effekseer_TextureLoader(TextureLoaderCallback loader)
{
	PyObject* arglist;
	arglist = Py_BuildValue("(si)", loader.name, loader.type);
	PyObject* result = PyEval_CallObject(onTextureLoaderCallBack, arglist);

	Effekseer::TextureData* textureData = new Effekseer::TextureData();;
	if (result)
	{
		if (PyTuple_Check(result)) {
			int numAttr = (int)PyTuple_Size(result);
			if (numAttr != 4) {
				PyErr_SetString(PyExc_TypeError, "4 Parameters : width(int) | height(int) | texture_id(int) | has_mipmap(bool)");
				return NULL;
			}

			textureData->Width = PyLong_AsLong(PyTuple_GET_ITEM(result, 0));
			textureData->Height = PyLong_AsLong(PyTuple_GET_ITEM(result, 1));
			textureData->UserID = PyLong_AsLong(PyTuple_GET_ITEM(result, 2));
			textureData->HasMipmap = PyLong_AsLong(PyTuple_GET_ITEM(result, 3));
		}
	}

	Py_DECREF(arglist);
	Py_XDECREF(result);

	return textureData;
}

PyObject* effekseer_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	effekseer_obj* self = NULL;

	self = (effekseer_obj*)type->tp_alloc(type, 0);
	self->effekseer = new pyxieEffekseer();
	self->effekseer->init();

	return (PyObject*)self;
}

void effekseer_dealloc(effekseer_obj* self)
{
	self->effekseer->release();
	Py_TYPE(self)->tp_free(self);
}

PyObject* effekseer_str(effekseer_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "effekseer object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

PyObject* effekseer_registerTextureLoader(PyTypeObject* type, PyObject* args)
{
	effekseer_obj* self = NULL;

	if (!PyArg_ParseTuple(args, "O", &onTextureLoaderCallBack))
		return NULL;

	if (!PyCallable_Check(onTextureLoaderCallBack))
	{
		PyErr_SetString(PyExc_TypeError, "Callback function must be a callable object!");
		return NULL;
	}
	Py_XINCREF(onTextureLoaderCallBack);

	pyxieEffekseer::setTextureLoader(effekseer_TextureLoader);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_Shoot(effekseer_obj* self, PyObject* args)
{
	float dt = 0.0f;
	int clear = false;
	if (!PyArg_ParseTuple(args, "f|i", &dt, &clear))
		return NULL;

	self->effekseer->update(dt);
	self->effekseer->render(clear);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_Add(effekseer_obj* self, PyObject* args)
{
	PyObject* position = nullptr;
	char* name;
	if (!PyArg_ParseTuple(args, "s|O", &name, &position))
		return NULL;

	int d1;
	float buff[3] = {0.0, 0.0, 0.0};
	float* v1 = pyObjToFloat((PyObject*)position, buff, d1);

	int handle = self->effekseer->play(name , *((Effekseer::Vector3D*)v1));
	return PyLong_FromLong(handle);
}

PyObject* effekseer_Remove(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;
	
	self->effekseer->stop(handle);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_StopAllEffects(effekseer_obj* self)
{
	self->effekseer->stopAll();

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_SetTargetLocation(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	float x, y, z;
	if (!PyArg_ParseTuple(args, "ifff", &handle, &x, &y, &z))
		return NULL;
	
	self->effekseer->SetTargetLocation(handle, x, y, z);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_GetLocation(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;

	auto location = self->effekseer->GetLocation(handle);
	PyObject* at = Py_BuildValue("(fff)", location.X, location.Y, location.Z);
	return at;
}

PyObject* effekseer_SetLocation(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	float x, y, z;
	if (!PyArg_ParseTuple(args, "ifff", &handle, &x, &y, &z))
		return NULL;

	self->effekseer->SetLocation(handle, x, y, z);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_SetRotation(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	float x, y, z;
	if (!PyArg_ParseTuple(args, "ifff", &handle, &x, &y, &z))
		return NULL;

	self->effekseer->SetRotation(handle, x, y, z);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_SetScale(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	float x, y, z;
	if (!PyArg_ParseTuple(args, "ifff", &handle, &x, &y, &z))
		return NULL;

	self->effekseer->SetScale(handle, x, y, z);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_SetColor(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	int red, green, blue, alpha;
	if (!PyArg_ParseTuple(args, "iiiii", &handle, &red, &green, &blue, &alpha))
		return NULL;

	self->effekseer->SetAllColor(handle, Color(red, green, blue, alpha));

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_SetSpeed(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	float speed;
	if (!PyArg_ParseTuple(args, "if", &handle, &speed))
		return NULL;

	self->effekseer->SetSpeed(handle, speed);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_GetSpeed(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;

	return PyFloat_FromDouble(self->effekseer->GetSpeed(handle));
}

PyObject* effekseer_IsPlaying(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;

	return PyLong_FromLong(self->effekseer->IsPlaying(handle));
}

PyObject* effekseer_SetPause(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	int paused = 0;
	if (!PyArg_ParseTuple(args, "ii", &handle, &paused))
		return NULL;

	self->effekseer->SetPause(handle, paused);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_GetPause(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;

	return PyLong_FromLong(self->effekseer->GetPause(handle));
}

PyObject* effekseer_SetShown(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	int shown = 0;
	if (!PyArg_ParseTuple(args, "ii", &handle, &shown))
		return NULL;

	self->effekseer->SetShown(handle, shown);

	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* effekseer_GetShown(effekseer_obj* self, PyObject* args)
{
	int handle = -1;
	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;

	return PyLong_FromLong(self->effekseer->GetShown(handle));
}

PyObject* effekseer_DrawCallCount(effekseer_obj* self)
{
	return PyLong_FromLong(self->effekseer->getDrawcallCount());
}

PyObject* effekseer_DrawVertexCount(effekseer_obj* self)
{
	return PyLong_FromLong(self->effekseer->getDrawVertexCount());
}

PyObject* effekseer_UpdateTime(effekseer_obj* self)
{
	return PyLong_FromLong(self->effekseer->getUpdateTime());
}

PyObject* effekseer_DrawTime(effekseer_obj* self)
{
	return PyLong_FromLong(self->effekseer->getDrawTime());
}

PyObject* effekseer_getViewport(effekseer_obj* self)
{
	PyObject* at = Py_BuildValue("(ff)", self->effekseer->GetViewport().X, self->effekseer->GetViewport().Y);
	return at;
}

int effekseer_setViewport(effekseer_obj* self, PyObject* value)
{
	float x, y;
	if (!PyArg_ParseTuple(value, "ff", &x, &y))
		return NULL;

	self->effekseer->SetViewport(Effekseer::Vector2D(x, y));
	return 0;
}

PyObject* effekseer_getViewSize(effekseer_obj* self)
{
	PyObject* at = Py_BuildValue("(ff)", self->effekseer->GetViewSize().X, self->effekseer->GetViewSize().Y);
	return at;
}

int effekseer_setViewSize(effekseer_obj* self, PyObject* value)
{
	float x, y;
	if (!PyArg_ParseTuple(value, "ff", &x, &y))
		return NULL;

	self->effekseer->SetViewSize(Effekseer::Vector2D(x, y));
	return 0;
}

PyObject* effekseer_getFramerate(effekseer_obj* self)
{
	return PyFloat_FromDouble(self->effekseer->GetFramerate());
}

int effekseer_setFramerate(effekseer_obj* self, PyObject* value)
{
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to desired framerate.");
		return -1;
	}
	self->effekseer->SetFramerate((float)PyFloat_AsDouble(value));
	return 0;
}

PyObject* effekseer_getOrtho(effekseer_obj* self)
{
	return PyFloat_FromDouble(self->effekseer->GetProjectionOrtho());
}

int effekseer_setOrtho(effekseer_obj* self, PyObject* value)
{
	self->effekseer->SetProjectionOrtho(PyLong_AsLong(value));
	return 0;
}

PyObject* effekseer_getAspect(effekseer_obj* self)
{
	return PyFloat_FromDouble(self->effekseer->GetProjectionAspect());
}

int effekseer_setAspect(effekseer_obj* self, PyObject* value)
{
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to projection aspect.");
		return -1;
	}
	self->effekseer->SetProjectionAspect((float)PyFloat_AsDouble(value));
	return 0;
}

PyObject* effekseer_getNear(effekseer_obj* self)
{
	return PyFloat_FromDouble(self->effekseer->GetProjectionAspect());
}

int effekseer_setNear(effekseer_obj* self, PyObject* value)
{
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to projection near.");
		return -1;
	}
	self->effekseer->SetProjectionNear((float)PyFloat_AsDouble(value));
	return 0;
}

PyObject* effekseer_getFar(effekseer_obj* self)
{
	return PyFloat_FromDouble(self->effekseer->GetProjectionFar());
}

int effekseer_setFar(effekseer_obj* self, PyObject* value)
{
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to projection far.");
		return -1;
	}
	self->effekseer->SetProjectionFar((float)PyFloat_AsDouble(value));
	return 0;
}

PyObject* effekseer_getFov(effekseer_obj* self)
{
	return PyFloat_FromDouble(self->effekseer->GetProjectionFov());
}

int effekseer_setFov(effekseer_obj* self, PyObject* value)
{
	if (!(PyFloat_Check(value) || PyLong_Check(value))) {
		PyErr_SetString(PyExc_TypeError, "Only float value can be set to projection fov.");
		return -1;
	}
	self->effekseer->SetProjectionFov((float)PyFloat_AsDouble(value));
	return 0;
}

PyObject* effekseer_getEye(effekseer_obj* self)
{
	PyObject* eye = Py_BuildValue("(fff)", self->effekseer->GetCameraEye().X, self->effekseer->GetCameraEye().Y, self->effekseer->GetCameraEye().Z);
	return eye;
}

int effekseer_setEye(effekseer_obj* self, PyObject* value)
{	
	float x, y, z;
	if (!PyArg_ParseTuple(value, "fff", &x, &y, &z))
		return NULL;

	self->effekseer->SetCameraEye(Effekseer::Vector3D(x, y, z));
	return 0;
}

PyObject* effekseer_getAt(effekseer_obj* self)
{
	PyObject* at = Py_BuildValue("(fff)", self->effekseer->GetCameraAt().X, self->effekseer->GetCameraAt().Y, self->effekseer->GetCameraAt().Z);
	return at;
}

int effekseer_setAt(effekseer_obj* self, PyObject* value)
{
	float x, y, z;
	if (!PyArg_ParseTuple(value, "fff", &x, &y, &z))
		return NULL;

	self->effekseer->SetCameraAt(Effekseer::Vector3D(x, y, z));
	return 0;
}

PyObject* effekseer_getUp(effekseer_obj* self)
{
	PyObject* up = Py_BuildValue("(fff)", self->effekseer->GetCameraUp().X, self->effekseer->GetCameraUp().Y, self->effekseer->GetCameraUp().Z);
	return up;
}

int effekseer_setUp(effekseer_obj* self, PyObject* value)
{
	float x, y, z;
	if (!PyArg_ParseTuple(value, "fff", &x, &y, &z))
		return NULL;

	self->effekseer->SetCameraUp(Effekseer::Vector3D(x, y, z));
	return 0;
}

PyMethodDef effekseer_methods[] = {
	{ "texture_loader", (PyCFunction)effekseer_registerTextureLoader, METH_VARARGS, effekseerTextureLoader_doc },
	{ "shoot", (PyCFunction)effekseer_Shoot, METH_VARARGS, effekseerShoot_doc },
	{ "add", (PyCFunction)effekseer_Add, METH_VARARGS, effekseerAdd_doc },
	{ "remove", (PyCFunction)effekseer_Remove, METH_VARARGS, effekseerRemove_doc },
	{ "stop_all_effects", (PyCFunction)effekseer_StopAllEffects, METH_NOARGS, effekseerRemove_doc },
	{ "drawcall_count", (PyCFunction)effekseer_DrawCallCount, METH_NOARGS, effekseerDrawCallCount_doc },
	{ "vertex_count", (PyCFunction)effekseer_DrawVertexCount, METH_NOARGS, effekseerDrawVertexCount_doc },
	{ "update_time", (PyCFunction)effekseer_UpdateTime, METH_NOARGS, effekseerUpdateTime_doc },
	{ "draw_time", (PyCFunction)effekseer_DrawTime, METH_NOARGS, effekseerDrawTime_doc },
	{ "set_target_location", (PyCFunction)effekseer_SetTargetLocation, METH_VARARGS, effekseerSetTargetLocation_doc },
	{ "get_location", (PyCFunction)effekseer_GetLocation, METH_VARARGS, effekseerGetLocation_doc },
	{ "set_location", (PyCFunction)effekseer_SetLocation, METH_VARARGS, effekseerSetLocation_doc },
	{ "set_rotation", (PyCFunction)effekseer_SetRotation, METH_VARARGS, effekseerSetRotation_doc },
	{ "set_scale", (PyCFunction)effekseer_SetScale, METH_VARARGS, effekseerSetScale_doc },
	{ "set_color", (PyCFunction)effekseer_SetColor, METH_VARARGS, effekseerSetColor_doc },
	{ "get_speed", (PyCFunction)effekseer_GetSpeed, METH_VARARGS, effekseerGetSpeed_doc },
	{ "set_speed", (PyCFunction)effekseer_SetSpeed, METH_VARARGS, effekseerSetSpeed_doc },
	{ "is_playing", (PyCFunction)effekseer_IsPlaying, METH_VARARGS, effekseerIsPlaying_doc },
	{ "set_pause", (PyCFunction)effekseer_SetPause, METH_VARARGS, effekseerSetPause_doc },
	{ "get_pause", (PyCFunction)effekseer_GetPause, METH_VARARGS, effekseerGetPause_doc },
	{ "set_shown", (PyCFunction)effekseer_SetShown, METH_VARARGS, effekseerSetShown_doc },
	{ "get_shown", (PyCFunction)effekseer_GetShown, METH_VARARGS, effekseerGetShown_doc },
	{ NULL,	NULL }
};

PyGetSetDef effekseer_getsets[] = {
	{ const_cast<char*>("projection_ortho"), (getter)effekseer_getOrtho, (setter)effekseer_setOrtho, projection_ortho_doc, NULL },
	//{ const_cast<char*>("projection_aspect"), (getter)effekseer_getAspect, (setter)effekseer_setAspect, projection_aspect_doc, NULL },
	{ const_cast<char*>("projection_viewport"), (getter)effekseer_getViewport, (setter)effekseer_setViewport, projection_viewport_doc, NULL },
	{ const_cast<char*>("projection_viewsize"), (getter)effekseer_getViewSize, (setter)effekseer_setViewSize, projection_viewsize_doc, NULL },
	{ const_cast<char*>("projection_near"), (getter)effekseer_getNear, (setter)effekseer_setNear, projection_near_doc, NULL },
	{ const_cast<char*>("projection_far"), (getter)effekseer_getFar, (setter)effekseer_setFar, projection_far_doc, NULL },
	{ const_cast<char*>("projection_fov"), (getter)effekseer_getFov, (setter)effekseer_setFov, projection_fov_doc, NULL },
	{ const_cast<char*>("camera_eye"), (getter)effekseer_getEye, (setter)effekseer_setEye, camera_eye_doc, NULL },
	{ const_cast<char*>("camera_at"), (getter)effekseer_getAt, (setter)effekseer_setAt, camera_at_doc, NULL },
	{ const_cast<char*>("camera_up"), (getter)effekseer_getUp, (setter)effekseer_setUp, camera_up_doc, NULL },
	{ const_cast<char*>("framerate"), (getter)effekseer_getFramerate, (setter)effekseer_setFramerate, framerate_doc, NULL },
	{ NULL, NULL }
};

PyTypeObject EffekseerType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeEffekseer",						/* tp_name */
	sizeof(effekseer_obj),				/* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)effekseer_dealloc,		/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)effekseer_str,			/* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	0,									/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	effekseer_methods,					/* tp_methods */
	0,                                  /* tp_members */
	effekseer_getsets,					/* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	effekseer_new,						/* tp_new */
	0,									/* tp_free */
};


static PyModuleDef effekseer_module = {
	PyModuleDef_HEAD_INIT,
	"igeEffekseer",							// Module name to use with Python import statements
	"Effekseer Module.",					// Module description
	0,
	effekseer_methods						// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igeEffekseer() {
	PyObject* module = PyModule_Create(&effekseer_module);

	if (PyType_Ready(&EffekseerType) < 0) return NULL;

	Py_INCREF(&EffekseerType);
	PyModule_AddObject(module, "particle", (PyObject*)&EffekseerType);

	return module;
}