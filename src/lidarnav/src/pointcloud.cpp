#include <ros/ros.h>
#include <tf/transform_listener.h>
#include <laser_geometry/laser_geometry.h>

class PointClouder {
public:
    PointClouder();
    void scan_cb(const sensor_msgs::LaserScan::ConstPtr &scan);
private:
    ros::NodeHandle node;
    laser_geometry::LaserProjection proj;
    tf::TransformListener tf_ls;

    ros::Publisher pointcloud_pub;
    ros::Subscriber scan_sub;
};

PointClouder::PointClouder() {
    scan_sub = node.subscribe<sensor_msgs::LaserScan>("scan", 100, &PointClouder::scan_cb, this);
    pointcloud_pub = node.advertise<sensor_msgs::PointCloud2>("cloud", 100, false);
}

void PointClouder::scan_cb(const sensor_msgs::LaserScan::ConstPtr &scan) {
    sensor_msgs::PointCloud2 cloud;

    try {
        proj.transformLaserScanToPointCloud("base_link", *scan, cloud, tf_ls);
    } catch (tf2::ExtrapolationException e) {
        ROS_WARN("%s", e.what());
    } 

    pointcloud_pub.publish(cloud);
}


int main(int argc, char **argv) {
    ros::init(argc, argv, "pointcloud");

    PointClouder pc;

    ros::spin();
    return 0;
}
