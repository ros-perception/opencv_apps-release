%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/jazzy/.*$
%global __requires_exclude_from ^/opt/ros/jazzy/.*$

%global __cmake_in_source_build 1

Name:           ros-jazzy-opencv-apps
Version:        3.1.0
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS opencv_apps package

License:        BSD
URL:            https://ros-perception.github.io/opencv_apps/
Source0:        %{name}-%{version}.tar.gz

Requires:       curl
Requires:       libcurl-devel
Requires:       ros-jazzy-class-loader
Requires:       ros-jazzy-cv-bridge
Requires:       ros-jazzy-geometry-msgs
Requires:       ros-jazzy-image-transport
Requires:       ros-jazzy-image-view
Requires:       ros-jazzy-message-filters
Requires:       ros-jazzy-nav-msgs
Requires:       ros-jazzy-rclcpp
Requires:       ros-jazzy-rclcpp-components
Requires:       ros-jazzy-rosidl-default-runtime
Requires:       ros-jazzy-sensor-msgs
Requires:       ros-jazzy-std-msgs
Requires:       ros-jazzy-std-srvs
Requires:       ros-jazzy-tf2-ros
Requires:       ros-jazzy-vision-msgs
Requires:       ros-jazzy-visualization-msgs
Requires:       ros-jazzy-ros-workspace
BuildRequires:  curl
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  glibc-static
BuildRequires:  libcurl-devel
BuildRequires:  libstdc++-devel
BuildRequires:  libstdc++-static
BuildRequires:  ros-jazzy-ament-cmake
BuildRequires:  ros-jazzy-class-loader
BuildRequires:  ros-jazzy-cv-bridge
BuildRequires:  ros-jazzy-geometry-msgs
BuildRequires:  ros-jazzy-image-transport
BuildRequires:  ros-jazzy-message-filters
BuildRequires:  ros-jazzy-nav-msgs
BuildRequires:  ros-jazzy-rclcpp
BuildRequires:  ros-jazzy-rclcpp-components
BuildRequires:  ros-jazzy-ros-environment
BuildRequires:  ros-jazzy-rosidl-default-generators
BuildRequires:  ros-jazzy-sensor-msgs
BuildRequires:  ros-jazzy-std-msgs
BuildRequires:  ros-jazzy-std-srvs
BuildRequires:  ros-jazzy-tf2-ros
BuildRequires:  ros-jazzy-vision-msgs
BuildRequires:  ros-jazzy-visualization-msgs
BuildRequires:  ros-jazzy-ros-workspace
BuildRequires:  ros-jazzy-rosidl-typesupport-fastrtps-c
BuildRequires:  ros-jazzy-rosidl-typesupport-fastrtps-cpp
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}
Provides:       ros-jazzy-rosidl-interface-packages(member)

%if 0%{?with_tests}
BuildRequires:  python%{python3_pkgversion}-numpy
BuildRequires:  python3-opencv
BuildRequires:  ros-jazzy-ament-index-python
BuildRequires:  ros-jazzy-compressed-image-transport
BuildRequires:  ros-jazzy-image-proc
BuildRequires:  ros-jazzy-image-publisher
BuildRequires:  ros-jazzy-launch-ros
BuildRequires:  ros-jazzy-launch-testing-ament-cmake
BuildRequires:  ros-jazzy-rosidl-runtime-py
BuildRequires:  ros-jazzy-tf2-msgs
BuildRequires:  ros-jazzy-topic-tools
%endif

%if 0%{?with_weak_deps}
Supplements:    ros-jazzy-rosidl-interface-packages(all)
%endif

%description
opencv_apps provides various nodes that run internally OpenCV's functionalities
and publish the result as ROS topics. With opencv_apps, you can skip writing
OpenCV application codes for a lot of its functionalities by simply running a
launch file that corresponds to OpenCV's functionality you want. You can have a
look at all launch files provided here (be sure to choose the correct branch. As
of Sept. 2016 indigo branch is used for ROS Indigo, Jade, and Kinetic distros).
The nodes are documented in the documentation (and the wiki for ROS 1). The most
of code is originally taken from
https://github.com/Itseez/opencv/tree/master/samples/cpp

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/jazzy" \
    -DAMENT_PREFIX_PATH="/opt/ros/jazzy" \
    -DCMAKE_PREFIX_PATH="/opt/ros/jazzy" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/jazzy

%changelog
* Mon Nov 23 2026 Kei Okada <kei.okada@gmail.com> - 3.1.0-1
- Autogenerated by Bloom

* Sat Nov 14 2026 Kei Okada <kei.okada@gmail.com> - 3.0.0-1
- Autogenerated by Bloom

