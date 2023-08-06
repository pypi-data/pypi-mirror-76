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


#include <pyclustering/cluster/somsc_data.hpp>

#include <pyclustering/nnet/som.hpp>


namespace pyclustering {

namespace clst {


/*!

@class   somsc somsc.hpp pyclustering/cluster/somsc.hpp

@brief   The class represents a simple clustering algorithm based on the self-organized feature map.
@details This algorithm uses amount of clusters that should be allocated as a size of SOM map. Captured 
           objects by neurons are considered as clusters. The algorithm is designed to process data with Gaussian 
           distribution that has spherical forms.

*/
class somsc {
private:
    std::size_t         m_amount_clusters   = 0;

    std::size_t         m_epoch             = 0;

public:
    /**
     *
     * @brief Default constructor to create algorithm instance.
     *
     */
    somsc() = default;

    /**
     *
     * @brief Default copy constructor to create algorithm instance.
     *
     */
    somsc(const somsc & p_other) = default;

    /**
     *
     * @brief Default move constructor to create algorithm instance.
     *
     */
    somsc(somsc && p_other) = default;

    /**
     *
     * @brief Creates algorithm with specified parameters.
     *
     * @param[in] p_amount_clusters: amount of clusters that should be allocated.
     * @param[in] p_epoch: maximum iterations for SOM learning process.
     *
     */
    somsc(const std::size_t p_amount_clusters, const std::size_t p_epoch = 100);

    /**
     *
     * @brief Default destructor to destroy algorithm instance.
     *
     */
    ~somsc() = default;

public:
    /**
    *
    * @brief    Performs cluster analysis of an input data.
    *
    * @param[in]  p_data: input data for cluster analysis.
    * @param[out] p_result: clustering result of an input data (consists of allocated clusters).
    *
    */
    void process(const dataset & p_data, somsc_data & p_result);
};


}

}
