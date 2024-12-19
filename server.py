from fastapi import FastAPI, File, UploadFile, HTTPException
import whisper
import librosa
import numpy as np
import io

app = FastAPI()

# Загрузка модели Whisper
model = whisper.load_model("base")

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    print(file.content_type)
    """
    Обработка аудиофайла для транскрипции и поиска команд.
    """
    if file.content_type not in ["audio/wave", "audio/mpeg"]:
        raise HTTPException(status_code=400, detail="Файл должен быть в формате .wav или .mp3")
    
    try:
        # Читаем загруженный файл
        audio_bytes = await file.read()
        
        # Загружаем аудио с помощью librosa
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=None)
        
        # Если стерео, конвертируем в моно
        if len(audio.shape) > 1 and audio.shape[0] == 2:
            audio = librosa.to_mono(audio)
        
        # Преобразуем частоту дискретизации, если необходимо
        if sr != 16000:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
        
        audio_numpy = np.array(audio).astype(np.float32)
        
        # Транскрибируем аудио
        transcription = model.transcribe(audio_numpy)
        text = transcription["text"]
        
        # Проверяем на наличие команд
        if "вперед" in text.lower():
            return {"command": "вперед"}
        elif "назад" in text.lower():
            return {"command": "назад"}
        else:
            return {"command": "Не найдено команд назад или вперед"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки файла: {str(e)}")

# Точка для проверки состояния сервера
@app.get("/")
def read_root():
    return {"message": "Сервер работает. Используйте /transcribe для обработки аудио."}
    