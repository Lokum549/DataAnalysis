cmake_minimum_required(VERSION 3.10)
project(Lab6)

set(CMAKE_CXX_STANDARD 17)

# Шукаємо OpenCV
find_package(OpenCV REQUIRED)

# Додаємо теку include для заголовних файлів
include_directories(include ${OpenCV_INCLUDE_DIRS})

# Збираємо всі .cpp файли з теки src
file(GLOB SOURCES "src/*.cpp")

# Створюємо виконуваний файл
add_executable(Lab6 ${SOURCES})

# Лінкуємо бібліотеки OpenCV
target_link_libraries(Lab6 ${OpenCV_LIBS})