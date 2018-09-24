cmake_minimum_required(VERSION 2.8.3)
project(refills_counting_image_saver)

find_package(catkin REQUIRED COMPONENTS message_generation std_msgs)

add_message_files(DIRECTORY msg FILES Floats.msg HeaderString.msg)
add_service_files(DIRECTORY srv FILES saveImage.srv)

generate_messages(DEPENDENCIES std_msgs)

catkin_package(CATKIN_DEPENDS message_runtime std_msgs)


catkin_install_python(PROGRAMS
  script/refills_counter_image_saver_server.py
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/script
)

