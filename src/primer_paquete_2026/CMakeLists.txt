cmake_minimum_required(VERSION 3.8)
project(primer_paquete_2026)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
"action/MyAction.action"
)

install(PROGRAMS
  ejercicio1/scripts/ejercicio1_publisher.py
  ejercicio1/scripts/ejercicio1_subscriber.py
  ejercicio2/scripts/ejercicio2_action_server.py
  ejercicio2/scripts/ejercicio2_action_client.py
  ejercicio5/scripts/gui_apply_torque.py
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY
  ejercicio4/robot_description
  ejercicio4/config
  DESTINATION share/${PROJECT_NAME}/ejercicio4
)

install(DIRECTORY
  crear_pkg/rviz
  crear_pkg/rqt
  DESTINATION share/${PROJECT_NAME}/crear_pkg
)

install(DIRECTORY
  ejercicio5/robot_description
  ejercicio5/config
  ejercicio5/models
  ejercicio5/worlds
  DESTINATION share/${PROJECT_NAME}/ejercicio5
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
