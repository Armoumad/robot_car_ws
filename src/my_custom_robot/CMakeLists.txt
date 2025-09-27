cmake_minimum_required(VERSION 3.8)
project(my_custom_robot)

# Options de compilation
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Dépendances
find_package(ament_cmake REQUIRED)

# Tests
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

# Installation des dossiers
install(
  DIRECTORY config launch urdf meshes worlds
  DESTINATION share/${PROJECT_NAME}
)

ament_package()