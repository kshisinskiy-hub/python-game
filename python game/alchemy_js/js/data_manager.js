import fs from 'fs';
import path from 'path';

export class DataManager {
    static loadConfig(filePath) {
        try {
            if (!fs.existsSync(filePath)) {
                throw new Error("Файл конфигурации не найден на диске.");
            }
            const rawData = fs.readFileSync(filePath, 'utf-8');
            const config = JSON.parse(rawData);
            DataManager._validate(config);
            return config;
        } catch (e) {
            throw new Error(`Ошибка загрузки или валидации JSON: ${e.message}`);
        }
    }

    static _validate(config) {
        if (!config.initial_elements || !Array.isArray(config.initial_elements)) {
            throw new Error("Поле 'initial_elements' отсутствует или не является массивом.");
        }
        if (!config.recipes || typeof config.recipes !== 'object') {
            throw new Error("Поле 'recipes' отсутствует или не является объектом.");
        }
    }
}