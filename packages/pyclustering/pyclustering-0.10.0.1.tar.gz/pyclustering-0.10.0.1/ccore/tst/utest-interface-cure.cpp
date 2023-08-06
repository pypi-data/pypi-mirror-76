/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2020
* @copyright GNU Public License
*
* GNU_PUBLIC_LICENSE
*   pyclustering is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   pyclustering is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/

#include <gtest/gtest.h>

#include <pyclustering/interface/cure_interface.h>
#include <pyclustering/interface/pyclustering_package.hpp>

#include "samples.hpp"
#include "utenv_utils.hpp"
#include "utenv_check.hpp"

#include <memory>


using namespace pyclustering;


TEST(utest_interface_cure, cure_api) {
    std::shared_ptr<pyclustering_package> sample = pack(dataset({ { 1 }, { 2 }, { 3 }, { 10 }, { 11 }, { 12 } }));

    void * cure_result = cure_algorithm(sample.get(), 2, 1, 0.5);
    ASSERT_NE(nullptr, cure_result);

    std::shared_ptr<pyclustering_package> clusters(cure_get_clusters(cure_result));
    ASSERT_EQ(2U, clusters->size);

    std::shared_ptr<pyclustering_package> representors(cure_get_representors(cure_result));
    ASSERT_EQ(2U, representors->size);

    std::shared_ptr<pyclustering_package> means(cure_get_means(cure_result));
    ASSERT_EQ(2U, means->size);

    cure_data_destroy(cure_result);
}


TEST(utest_interface_cure, cure_api_long_result) {
    auto sample_sptr = fcps_sample_factory::create_sample(FCPS_SAMPLE::HEPTA);
    std::shared_ptr<pyclustering_package> sample = pack(*sample_sptr);

    void * cure_result = cure_algorithm(sample.get(), 7, 1, 0.3);
    ASSERT_NE(nullptr, cure_result);

    std::shared_ptr<pyclustering_package> clusters(cure_get_clusters(cure_result));
    ASSERT_EQ(7U, clusters->size);

    std::shared_ptr<pyclustering_package> representors(cure_get_representors(cure_result));
    ASSERT_EQ(7U, representors->size);

    std::shared_ptr<pyclustering_package> means(cure_get_means(cure_result));
    ASSERT_EQ(7U, means->size);

    cure_data_destroy(cure_result);
}