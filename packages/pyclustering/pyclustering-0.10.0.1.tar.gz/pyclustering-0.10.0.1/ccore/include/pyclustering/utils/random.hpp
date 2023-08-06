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


#pragma once


namespace pyclustering {

namespace utils {

namespace random {


/**
 *
 * @brief   Returns random value in specified range using uniform distribution.
 *
 * @param[in] p_from: Mean.
 * @param[in] p_to:   Standard deviation.
 *
 * @return  Returns random variable.
 *
 */
double generate_uniform_random(const double p_from = 0.0, const double p_to = 1.0);


}

}

}