/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    pyclustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyclustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

*/

#pragma once


#include <vector>
#include <list>

#include <pyclustering/cluster/cluster_data.hpp>
#include <pyclustering/container/adjacency_matrix.hpp>

#include <pyclustering/definitions.hpp>


using namespace pyclustering::container;


namespace pyclustering {

namespace clst {


using rock_data = cluster_data;

/*!

@class   rock rock.hpp pyclustering/cluster/rock.hpp

@brief   The class represents a clustering algorithm ROCK.
@details Implementation of the algorithm is based on the paper @cite inproceedings::rock::1.

*/
class rock {
private:
    /* for optimization list representation is of clusters is used and than
     * it is moved to output result */
    using rock_cluster_sequence = std::list<cluster>;

private:
    adjacency_matrix        m_adjacency_matrix;

    double                  m_radius;

    double                  m_degree_normalization;

    size_t                  m_number_clusters;

    rock_cluster_sequence   m_clusters;

public:
    /**
    *
    * @brief    Default constructor of clustering algorithm.
    *
    */
    rock();

    /**
    *
    * @brief    Creates ROCK solver in line with specified parameters of the algorithm.
    *
    * @param[in] radius: connectivity radius (similarity threshold), points are neighbors if distance between them is less than connectivity radius.
    * @param[in] number_clusters: amount of clusters that should be allocated.
    * @param[in] threshold: defines degree of normalization that influences on choice of clusters for merging during processing.
    *
    */
    rock(const double radius, const std::size_t number_clusters, const double threshold);

    /**
    *
    * @brief    Default destructor of the algorithm.
    *
    */
    ~rock() = default;

public:
    /**
    *
    * @brief    Performs cluster analysis of an input data.
    *
    * @param[in]  p_data: input data for cluster analysis.
    * @param[out] p_result: clustering result of an input data.
    *
    */
    void process(const dataset & p_data, rock_data & p_result);

private:
    /**
    *
    * @brief    Creates adjacency matrix where each element described existence of link between points (means that points are neighbors).
    *
    * @param[in]  p_data: input data for cluster analysis.
    *
    */
    void create_adjacency_matrix(const dataset & p_data);

    /**
    *
    * @brief    Finds two clusters that are most suitable candidates for merging and than merges them.
    *
    */
    bool merge_cluster();

    /**
    *
    * @brief    Returns number of link between two clusters.
    * @details  Link between objects (points) exists only if distance between them less than connectivity radius.
    *
    * @param[in] cluster1: the first cluster.
    * @param[in] cluster2: the second cluster.
    *
    * @return Number of links between two clusters.
    *
    */
    size_t calculate_links(const cluster & cluster1, const cluster & cluster2) const;

    /**
    *
    * @brief    Calculates coefficient 'goodness measurement' between two clusters.
    * @details  The coefficient defines level of suitability of clusters for merging.
    *
    * @param[in] cluster1: the first cluster.
    * @param[in] cluster2: the second cluster.
    *
    * @return Goodness measure between two clusters.
    *
    */
    double calculate_goodness(const cluster & cluster1, const cluster & cluster2) const;
};


}

}