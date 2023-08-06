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


#include <pyclustering/utils/stats.hpp>


namespace pyclustering {

namespace utils {

namespace stats {


std::vector<double> critical_values(const std::size_t p_data_size) {
    std::vector<double> result = { 0.576, 0.656, 0.787, 0.918, 1.092 };
    const double size = static_cast<const double>(p_data_size);
    for (auto & value : result) {
        value /= (1.0 + 4.0 / size - 25.0 / size / size);
    }

    return result;
}


}

}

}