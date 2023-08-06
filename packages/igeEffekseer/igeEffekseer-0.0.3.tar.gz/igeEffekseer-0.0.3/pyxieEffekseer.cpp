
#if defined _WIN32
#   include <glew.h>
#   include <gl/gl.h>
#   include <gl/glu.h>
#	include <wglew.h>
#endif

#include "pyxieEffekseer.h"
#include <string>

TextureLoaderFunc pyxieEffekseer::textureLoaderFunc = nullptr;

class pyxieTextureLoader : public ::Effekseer::TextureLoader
{
public:
	pyxieTextureLoader();
	virtual ~pyxieTextureLoader();

public:
	Effekseer::TextureData* Load(const EFK_CHAR* path, ::Effekseer::TextureType textureType) override;
	void Unload(Effekseer::TextureData* data) override;
};


pyxieTextureLoader::pyxieTextureLoader()
{
}

pyxieTextureLoader::~pyxieTextureLoader()
{
}

static std::u16string getFilenameWithoutExt(const char16_t* path)
{
	int start = 0;
	int end = 0;

	for (int i = start; path[i] != 0; i++)
	{
		if (path[i] == u'.')
		{
			end = i;
		}
	}

	std::vector<char16_t> ret;

	for (int i = start; i < end; i++)
	{
		ret.push_back(path[i]);
	}
	ret.push_back(0);

	return std::u16string(ret.data());
}

Effekseer::TextureData* pyxieTextureLoader::Load(const EFK_CHAR* path, ::Effekseer::TextureType textureType)
{
	auto _path = getFilenameWithoutExt(path);	

	char path_[300];
	Effekseer::ConvertUtf16ToUtf8((int8_t*)path_, 300, (const int16_t*)_path.c_str());
	if (pyxieEffekseer::textureLoaderFunc != nullptr)
	{
		TextureLoaderCallback callback = { path_ , TextureLoaderType::LOAD};
		auto textureData = pyxieEffekseer::textureLoaderFunc(callback);

		return textureData;
	}
	return new Effekseer::TextureData();
}

void pyxieTextureLoader::Unload(Effekseer::TextureData* data)
{

}

pyxieEffekseer::pyxieEffekseer()
	: manager(nullptr)
	, renderer(nullptr)
	, desiredFramerate(60.0)
	, projection_ortho(false)
	, projection_fov(90)
	, projection_aspect(480.0 / 640.0)
	, projection_near(1.0)
	, projection_far(1000)
	, camera_eye(Effekseer::Vector3D(0.0, 0.0, -20.0))
	, camera_at(Effekseer::Vector3D(0.0, 0.0, 0.0))
	, camera_up(Effekseer::Vector3D(0.0, 1.0, 0.0))
	, viewport(Effekseer::Vector2D(-1.0, -1.0))
	, viewsize(Effekseer::Vector2D(480.0, 640.0))
{
}

pyxieEffekseer::~pyxieEffekseer()
{

}

void pyxieEffekseer::init()
{	
#if defined(_WIN32)
	renderer = EffekseerRendererGL::Renderer::Create(8000, EffekseerRendererGL::OpenGLDeviceType::OpenGL3);
#else
	renderer = EffekseerRendererGL::Renderer::Create(8000, EffekseerRendererGL::OpenGLDeviceType::OpenGLES3);
#endif

	manager = Effekseer::Manager::Create(8000);

	manager->SetSpriteRenderer(renderer->CreateSpriteRenderer());
	manager->SetRibbonRenderer(renderer->CreateRibbonRenderer());
	manager->SetRingRenderer(renderer->CreateRingRenderer());
	manager->SetTrackRenderer(renderer->CreateTrackRenderer());
	manager->SetModelRenderer(renderer->CreateModelRenderer());

	manager->SetTextureLoader(new pyxieTextureLoader()); //renderer->CreateTextureLoader() || new pyxieTextureLoader()
	manager->SetModelLoader(renderer->CreateModelLoader());
	manager->SetMaterialLoader(renderer->CreateMaterialLoader());
}

void pyxieEffekseer::release()
{
	if (manager != nullptr)
	{
		manager->Destroy();
		manager = nullptr;
	}

	if (renderer != nullptr)
	{
		renderer->Destroy();
		renderer = nullptr;
	}
}

void pyxieEffekseer::update(float dt)
{
	if (projection_ortho)
	{
		renderer->SetProjectionMatrix(::Effekseer::Matrix44().OrthographicRH(viewsize.X, viewsize.Y, projection_near, projection_far));
		renderer->SetCameraMatrix(Effekseer::Matrix44().LookAtRH(camera_eye, camera_at, camera_up));
	}
	else
	{
		renderer->SetProjectionMatrix(Effekseer::Matrix44().PerspectiveFovRH(projection_fov / 180.0f * 3.14f, projection_aspect, projection_near, projection_far));
		renderer->SetCameraMatrix(Effekseer::Matrix44().LookAtRH(camera_eye, camera_at, camera_up));
	}

	manager->Update(desiredFramerate * dt);
}

int pyxieEffekseer::play(const char* name, const Effekseer::Vector3D& position)
{
	EFK_CHAR path[300];
	Effekseer::ConvertUtf8ToUtf16((int16_t*)path, 300, (const int8_t*)name);

	auto _effect = Effekseer::Effect::Create(manager, path);

	return manager->Play(_effect, position);
}

void pyxieEffekseer::stop(int handle)
{
	if (manager->Exists(handle))
	{
		manager->StopEffect(handle);
	}
}

void pyxieEffekseer::stopAll()
{
	manager->StopAllEffects();
}

void pyxieEffekseer::clearScreen()
{
    glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);
}

void pyxieEffekseer::setup(bool isClear)
{
#if defined(__ANDROID__) || TARGET_OS_IPHONE
    int fbo = 0;
    glGetIntegerv(GL_FRAMEBUFFER_BINDING, &fbo);
    glBindFramebuffer(GL_FRAMEBUFFER, fbo);    
#endif   
	
	if (viewport.X > 0.0 && viewport.Y > 0.0)
	{
		glViewport(0, 0, viewport.X, viewport.Y);
	}

	if (isClear)
	{
		clearScreen();
	}
}

void pyxieEffekseer::render(bool isClear)
{
	setup(isClear);

	renderer->BeginRendering();
	manager->Draw();
	renderer->EndRendering();
}

int32_t pyxieEffekseer::getDrawcallCount()
{
	int32_t count = renderer->GetDrawCallCount();
	renderer->ResetDrawCallCount();

	return count;
}

int32_t pyxieEffekseer::getDrawVertexCount()
{
	int32_t count = renderer->GetDrawVertexCount();
	renderer->ResetDrawVertexCount();

	return count;
}

int32_t pyxieEffekseer::getUpdateTime()
{
	return manager->GetUpdateTime();
}

int32_t pyxieEffekseer::getDrawTime()
{
	return manager->GetDrawTime();
}

void pyxieEffekseer::setTextureLoader(TextureLoaderFunc loader)
{
	textureLoaderFunc = loader;
}

void pyxieEffekseer::SetTargetLocation(Handle handle, float x, float y, float z)
{
	manager->SetTargetLocation(handle, x, y, z);
}

const Vector3D& pyxieEffekseer::GetLocation(Handle handle)
{
	return manager->GetLocation(handle);
}
void pyxieEffekseer::SetLocation(Handle handle, float x, float y, float z)
{
	manager->SetLocation(handle, x, y, z);
}

void pyxieEffekseer::SetRotation(Handle handle, float x, float y, float z)
{
	manager->SetRotation(handle, x, y, z);
}

void pyxieEffekseer::SetScale(Handle handle, float x, float y, float z)
{
	manager->SetScale(handle, x, y, z);
}

void pyxieEffekseer::SetAllColor(Handle handle, Color color)
{
	manager->SetAllColor(handle, color);
}

void pyxieEffekseer::SetSpeed(Handle handle, float speed)
{
	manager->SetSpeed(handle, speed);
}

float pyxieEffekseer::GetSpeed(Handle handle)
{
	return manager->GetSpeed(handle);
}

bool pyxieEffekseer::IsPlaying(Handle handle)
{
	return manager->Exists(handle);
}

void pyxieEffekseer::SetPause(Handle handle, bool paused)
{
	manager->SetPaused(handle, paused);
}

bool pyxieEffekseer::GetPause(Handle handle)
{
	return manager->GetPaused(handle);
}

void pyxieEffekseer::SetShown(Handle handle, bool shown)
{
	manager->SetShown(handle, shown);
}

bool pyxieEffekseer::GetShown(Handle handle)
{
	return manager->GetShown(handle);
}