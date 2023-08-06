depends = ('ITKPyBase', 'ITKImageFeature', 'ITKCommon', )
templates = (
  ('HessianImageFilter', 'itk::HessianImageFilter', 'itkHessianImageFilterISS2', True, 'itk::Image< signed short,2 >'),
  ('HessianImageFilter', 'itk::HessianImageFilter', 'itkHessianImageFilterISS3', True, 'itk::Image< signed short,3 >'),
  ('HessianImageFilter', 'itk::HessianImageFilter', 'itkHessianImageFilterIUC2', True, 'itk::Image< unsigned char,2 >'),
  ('HessianImageFilter', 'itk::HessianImageFilter', 'itkHessianImageFilterIUC3', True, 'itk::Image< unsigned char,3 >'),
  ('HessianImageFilter', 'itk::HessianImageFilter', 'itkHessianImageFilterIUS2', True, 'itk::Image< unsigned short,2 >'),
  ('HessianImageFilter', 'itk::HessianImageFilter', 'itkHessianImageFilterIUS3', True, 'itk::Image< unsigned short,3 >'),
  ('HessianImageFilter', 'itk::HessianImageFilter', 'itkHessianImageFilterIF2', True, 'itk::Image< float,2 >'),
  ('HessianImageFilter', 'itk::HessianImageFilter', 'itkHessianImageFilterIF3', True, 'itk::Image< float,3 >'),
  ('HessianImageFilter', 'itk::HessianImageFilter', 'itkHessianImageFilterID2', True, 'itk::Image< double,2 >'),
  ('HessianImageFilter', 'itk::HessianImageFilter', 'itkHessianImageFilterID3', True, 'itk::Image< double,3 >'),
  ('ObjectnessMeasureImageFilter', 'itk::ObjectnessMeasureImageFilter', 'itkObjectnessMeasureImageFilterIF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('ObjectnessMeasureImageFilter', 'itk::ObjectnessMeasureImageFilter', 'itkObjectnessMeasureImageFilterIF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
  ('ObjectnessMeasureImageFilter', 'itk::ObjectnessMeasureImageFilter', 'itkObjectnessMeasureImageFilterID2ID2', True, 'itk::Image< double,2 >, itk::Image< double,2 >'),
  ('ObjectnessMeasureImageFilter', 'itk::ObjectnessMeasureImageFilter', 'itkObjectnessMeasureImageFilterID3ID3', True, 'itk::Image< double,3 >, itk::Image< double,3 >'),
)
snake_case_functions = ('objectness_measure_image_filter', 'hessian_image_filter', )
