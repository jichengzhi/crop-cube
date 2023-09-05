import cv2
import numpy as np
from scipy.spatial import cKDTree
from sklearn.decomposition import PCA


def sample_to_heatmap(points, x_adjust=0, y_adjust=0, z_threshold=None, nearest_k=3):
    # If a threshold is provided, keep only points with a z-coordinate above this threshold
    if z_threshold is not None:
        points = points[points[:, 2] > z_threshold]
        print('cropped')

    # Compute PCA
    pca = PCA(n_components=3)
    pca.fit(points)

    # The normal of the plane is the smallest principal component
    normal = pca.components_[-1]

    # The point on the plane can be the centroid of the point cloud
    centroid = np.mean(points, axis=0)

    # Now we can print the plane equation
    # The plane equation is of the form ax + by + cz + d = 0
    a, b, c = normal
    d = -centroid.dot(normal)
    print(f"The equation of the plane is {a:.5f}x + {b:.5f}y + {c:.5f}z + {d:.5f} = 0")

    # Get x, y, z coordinates
    x_coords = points[:, 0]
    y_coords = points[:, 1]
    z_coords = points[:, 2]

    # Calculate minimum and maximum values in x and y directions
    x_min, x_max = np.min(x_coords), np.max(x_coords)
    y_min, y_max = np.min(y_coords), np.max(y_coords)

    x_mid = (x_min + x_max) / 2 + x_adjust
    y_mid = (y_min + y_max) / 2 + y_adjust
    # The range of x and y values for the mesh grid
    x_range = np.linspace(x_mid - 15, x_mid + 15, 514)
    y_range = np.linspace(y_mid - 15, y_mid + 15, 514)

    x, y = np.meshgrid(x_range, y_range)

    # Compute corresponding z values for the plane
    z = (-a * x - b * y - d) / c

    tree = cKDTree(points)

    distances = []
    for point in np.vstack([x.flatten(), y.flatten(), z.flatten()]).T:
        # Find the three nearest points in the point cloud
        dists, idxs = tree.query(point, k=nearest_k)
        nearest_points = points[idxs]

        # For each nearest point, compute the distance to the point along the normal direction
        ds = []
        for nearest_point in nearest_points:
            displacement = nearest_point - point  # vector from point to nearest_point
            distance = np.dot(displacement, normal)  # project displacement onto normal
            ds.append(distance)
        distances.append(sum(ds) / len(ds))

    # 这里是用最小值纠正（normalisation）矩阵
    distances_array = (np.array(distances) - np.min(distances)) / 0.5 * 255
    distances_reshape = distances_array.reshape((514, 514))[1:513, 1:513].astype(int)

    return distances_reshape  # 这个就是image 直接save就行


# Create a heatmap using seaborn
def plot_heatmap(heatmap, save_path=None):
    cv2.imwrite(save_path, heatmap)
