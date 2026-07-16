@echo off
setlocal

set OUT_DIR=%~2
if "%OUT_DIR%"=="" set OUT_DIR=examples\outputs
if not exist "%OUT_DIR%" mkdir "%OUT_DIR%"

echo Writing test outputs to %OUT_DIR%

python scripts\project_woofmapped_dog_dog_asymmetric_synastry.py --source-dataset "%OUT_DIR%\brandi_bre_synastry_dataset.full.json" --dog-a-id "brandi" --dog-a-label "Brandi" --dog-b-id "bre" --dog-b-label "Bre" --output-mode standard --out "%OUT_DIR%\brandi_bre_synastry.woofmapped.dog-dog.asymmetric.json"

python scripts\project_woofmapped_dog_dog_asymmetric_synastry.py --source-dataset "%OUT_DIR%\bre_brandi_synastry_dataset.full.json" --dog-b-id "brandi" --dog-b-label "Brandi" --dog-a-id "bre" --dog-a-label "Bre" --output-mode standard --out "%OUT_DIR%\bre_brandi_synastry.woofmapped.dog-dog.asymmetric.json"