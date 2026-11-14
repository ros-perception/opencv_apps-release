%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/kilted/.*$
%global __requires_exclude_from ^/opt/ros/kilted/.*$

%global __cmake_in_source_build 1

Name:           ros-kilted-opencv-apps
Version:        3.0.0
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS opencv_apps package

License:        BSD
URL:            https://ros-perception.github.io/opencv_apps/
Source0:        %{name}-%{version}.tar.gz

Requires:       curl
Requires:       libcurl-devel
Requires:       ros-kilted-class-loader
Requires:       ros-kilted-cv-bridge
Requires:       ros-kilted-geometry-msgs
Requires:       ros-kilted-image-transport
Requires:       ros-kilted-image-view
Requires:       ros-kilted-message-filters
Requires:       ros-kilted-rclcpp
Requires:       ros-kilted-rclcpp-components
Requires:       ros-kilted-rosidl-default-runtime
Requires:       ros-kilted-sensor-msgs
Requires:       ros-kilted-std-msgs
Requires:       ros-kilted-std-srvs
Requires:       ros-kilted-ros-workspace
BuildRequires:  curl
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  glibc-static
BuildRequires:  libcurl-devel
BuildRequires:  libstdc++-devel
BuildRequires:  libstdc++-static
BuildRequires:  ros-kilted-ament-cmake
BuildRequires:  ros-kilted-class-loader
BuildRequires:  ros-kilted-cv-bridge
BuildRequires:  ros-kilted-geometry-msgs
BuildRequires:  ros-kilted-image-transport
BuildRequires:  ros-kilted-message-filters
BuildRequires:  ros-kilted-rclcpp
BuildRequires:  ros-kilted-rclcpp-components
BuildRequires:  ros-kilted-ros-environment
BuildRequires:  ros-kilted-rosidl-default-generators
BuildRequires:  ros-kilted-sensor-msgs
BuildRequires:  ros-kilted-std-msgs
BuildRequires:  ros-kilted-std-srvs
BuildRequires:  ros-kilted-ros-workspace
BuildRequires:  ros-kilted-rosidl-typesupport-fastrtps-c
BuildRequires:  ros-kilted-rosidl-typesupport-fastrtps-cpp
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}
Provides:       ros-kilted-rosidl-interface-packages(member)

%if 0%{?with_tests}
BuildRequires:  python%{python3_pkgversion}-numpy
BuildRequires:  python3-opencv
BuildRequires:  ros-kilted-ament-index-python
BuildRequires:  ros-kilted-compressed-image-transport
BuildRequires:  ros-kilted-image-proc
BuildRequires:  ros-kilted-image-publisher
BuildRequires:  ros-kilted-launch-ros
BuildRequires:  ros-kilted-launch-testing-ament-cmake
BuildRequires:  ros-kilted-rosidl-runtime-py
BuildRequires:  ros-kilted-topic-tools
%endif

%if 0%{?with_weak_deps}
Supplements:    ros-kilted-rosidl-interface-packages(all)
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
if [ -f "/opt/ros/kilted/setup.sh" ]; then . "/opt/ros/kilted/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/kilted" \
    -DAMENT_PREFIX_PATH="/opt/ros/kilted" \
    -DCMAKE_PREFIX_PATH="/opt/ros/kilted" \
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
if [ -f "/opt/ros/kilted/setup.sh" ]; then . "/opt/ros/kilted/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/kilted/setup.sh" ]; then . "/opt/ros/kilted/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/kilted

%changelog
* Sat Nov 14 2026 Kei Okada <kei.okada@gmail.com> - 3.0.0-1
- Autogenerated by Bloom

