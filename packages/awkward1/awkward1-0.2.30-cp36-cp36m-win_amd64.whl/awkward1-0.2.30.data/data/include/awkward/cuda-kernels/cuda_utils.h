// BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/master/LICENSE

#ifndef AWKWARD_CUDA_UTILS_H
#define AWKWARD_CUDA_UTILS_H

#include "awkward/common.h"

extern "C" {
  EXPORT_SYMBOL ERROR awkward_cuda_ptr_device_num(int& device_num,
                                                  void* ptr);

  EXPORT_SYMBOL ERROR awkward_cuda_ptr_device_name(std::string& device_name,
                                                   void* ptr);
}

#endif //AWKWARD_CUDA_UTILS_H
