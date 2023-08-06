/*
 * Library known_folder_location type test program
 *
 * Copyright (C) 2009-2020, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include <common.h>
#include <file_stream.h>
#include <memory.h>
#include <types.h>

#if defined( HAVE_STDLIB_H ) || defined( WINAPI )
#include <stdlib.h>
#endif

#include "lnk_test_libcerror.h"
#include "lnk_test_liblnk.h"
#include "lnk_test_macros.h"
#include "lnk_test_memory.h"
#include "lnk_test_unused.h"

#include "../liblnk/liblnk_known_folder_location.h"

uint8_t lnk_test_known_folder_location_data1[ 28 ] = {
	0x1c, 0x00, 0x00, 0x00, 0x0b, 0x00, 0x00, 0xa0, 0x90, 0xe2, 0x4d, 0x37, 0x3f, 0x12, 0x65, 0x45,
	0x91, 0x64, 0x39, 0xc4, 0x92, 0x5e, 0x46, 0x7b, 0x34, 0x00, 0x00, 0x00 };

#if defined( __GNUC__ ) && !defined( LIBLNK_DLL_IMPORT )

/* Tests the liblnk_known_folder_location_initialize function
 * Returns 1 if successful or 0 if not
 */
int lnk_test_known_folder_location_initialize(
     void )
{
	libcerror_error_t *error                              = NULL;
	liblnk_known_folder_location_t *known_folder_location = NULL;
	int result                                            = 0;

#if defined( HAVE_LNK_TEST_MEMORY )
	int number_of_malloc_fail_tests                       = 1;
	int number_of_memset_fail_tests                       = 1;
	int test_number                                       = 0;
#endif

	/* Test regular cases
	 */
	result = liblnk_known_folder_location_initialize(
	          &known_folder_location,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	LNK_TEST_ASSERT_IS_NOT_NULL(
	 "known_folder_location",
	 known_folder_location );

	LNK_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	result = liblnk_known_folder_location_free(
	          &known_folder_location,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	LNK_TEST_ASSERT_IS_NULL(
	 "known_folder_location",
	 known_folder_location );

	LNK_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test error cases
	 */
	result = liblnk_known_folder_location_initialize(
	          NULL,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	LNK_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	known_folder_location = (liblnk_known_folder_location_t *) 0x12345678UL;

	result = liblnk_known_folder_location_initialize(
	          &known_folder_location,
	          &error );

	known_folder_location = NULL;

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	LNK_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

#if defined( HAVE_LNK_TEST_MEMORY )

	for( test_number = 0;
	     test_number < number_of_malloc_fail_tests;
	     test_number++ )
	{
		/* Test liblnk_known_folder_location_initialize with malloc failing
		 */
		lnk_test_malloc_attempts_before_fail = test_number;

		result = liblnk_known_folder_location_initialize(
		          &known_folder_location,
		          &error );

		if( lnk_test_malloc_attempts_before_fail != -1 )
		{
			lnk_test_malloc_attempts_before_fail = -1;

			if( known_folder_location != NULL )
			{
				liblnk_known_folder_location_free(
				 &known_folder_location,
				 NULL );
			}
		}
		else
		{
			LNK_TEST_ASSERT_EQUAL_INT(
			 "result",
			 result,
			 -1 );

			LNK_TEST_ASSERT_IS_NULL(
			 "known_folder_location",
			 known_folder_location );

			LNK_TEST_ASSERT_IS_NOT_NULL(
			 "error",
			 error );

			libcerror_error_free(
			 &error );
		}
	}
	for( test_number = 0;
	     test_number < number_of_memset_fail_tests;
	     test_number++ )
	{
		/* Test liblnk_known_folder_location_initialize with memset failing
		 */
		lnk_test_memset_attempts_before_fail = test_number;

		result = liblnk_known_folder_location_initialize(
		          &known_folder_location,
		          &error );

		if( lnk_test_memset_attempts_before_fail != -1 )
		{
			lnk_test_memset_attempts_before_fail = -1;

			if( known_folder_location != NULL )
			{
				liblnk_known_folder_location_free(
				 &known_folder_location,
				 NULL );
			}
		}
		else
		{
			LNK_TEST_ASSERT_EQUAL_INT(
			 "result",
			 result,
			 -1 );

			LNK_TEST_ASSERT_IS_NULL(
			 "known_folder_location",
			 known_folder_location );

			LNK_TEST_ASSERT_IS_NOT_NULL(
			 "error",
			 error );

			libcerror_error_free(
			 &error );
		}
	}
#endif /* defined( HAVE_LNK_TEST_MEMORY ) */

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( known_folder_location != NULL )
	{
		liblnk_known_folder_location_free(
		 &known_folder_location,
		 NULL );
	}
	return( 0 );
}

/* Tests the liblnk_known_folder_location_free function
 * Returns 1 if successful or 0 if not
 */
int lnk_test_known_folder_location_free(
     void )
{
	libcerror_error_t *error = NULL;
	int result               = 0;

	/* Test error cases
	 */
	result = liblnk_known_folder_location_free(
	          NULL,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	LNK_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	return( 0 );
}

/* Tests the liblnk_known_folder_location_read_data_block function
 * Returns 1 if successful or 0 if not
 */
int lnk_test_known_folder_location_read_data_block(
     void )
{
	libcerror_error_t *error                              = NULL;
	liblnk_data_block_t *data_block                       = NULL;
	liblnk_known_folder_location_t *known_folder_location = NULL;
	void *memcpy_result                                   = NULL;
	int result                                            = 0;

	/* Initialize test
	 */
	result = liblnk_known_folder_location_initialize(
	          &known_folder_location,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	LNK_TEST_ASSERT_IS_NOT_NULL(
	 "known_folder_location",
	 known_folder_location );

	LNK_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Initialize data block
	 */
	result = liblnk_data_block_initialize(
	          &data_block,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	LNK_TEST_ASSERT_IS_NOT_NULL(
	 "data_block",
	 data_block );

	LNK_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	data_block->data_size = 28;

	data_block->data = (uint8_t *) memory_allocate(
	                                data_block->data_size );

	LNK_TEST_ASSERT_IS_NOT_NULL(
	 "data_block->data",
	 data_block->data );

	memcpy_result = memory_copy(
	                 data_block->data,
	                 lnk_test_known_folder_location_data1,
	                 data_block->data_size );

	LNK_TEST_ASSERT_IS_NOT_NULL(
	 "memcpy_result",
	 memcpy_result );

	/* Test regular cases
	 */
	result = liblnk_known_folder_location_read_data_block(
	          known_folder_location,
	          data_block,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	LNK_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test error cases
	 */
	result = liblnk_known_folder_location_read_data_block(
	          NULL,
	          data_block,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	LNK_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = liblnk_known_folder_location_read_data_block(
	          known_folder_location,
	          NULL,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	LNK_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	data_block->data_size = 8;

	result = liblnk_known_folder_location_read_data_block(
	          known_folder_location,
	          data_block,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	LNK_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	/* Clean up data block
	 */
	result = liblnk_data_block_free(
	          &data_block,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	LNK_TEST_ASSERT_IS_NULL(
	 "data_block",
	 data_block );

	LNK_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Clean up
	 */
	result = liblnk_known_folder_location_free(
	          &known_folder_location,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	LNK_TEST_ASSERT_IS_NULL(
	 "known_folder_location",
	 known_folder_location );

	LNK_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( data_block != NULL )
	{
		liblnk_data_block_free(
		 &data_block,
		 NULL );
	}
	if( known_folder_location != NULL )
	{
		liblnk_known_folder_location_free(
		 &known_folder_location,
		 NULL );
	}
	return( 0 );
}

/* Tests the liblnk_known_folder_location_read_data function
 * Returns 1 if successful or 0 if not
 */
int lnk_test_known_folder_location_read_data(
     void )
{
	libcerror_error_t *error                              = NULL;
	liblnk_known_folder_location_t *known_folder_location = NULL;
	int result                                            = 0;

	/* Initialize test
	 */
	result = liblnk_known_folder_location_initialize(
	          &known_folder_location,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	LNK_TEST_ASSERT_IS_NOT_NULL(
	 "known_folder_location",
	 known_folder_location );

	LNK_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test regular cases
	 */
	result = liblnk_known_folder_location_read_data(
	          known_folder_location,
	          lnk_test_known_folder_location_data1,
	          28,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	LNK_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	/* Test error cases
	 */
	result = liblnk_known_folder_location_read_data(
	          NULL,
	          lnk_test_known_folder_location_data1,
	          28,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	LNK_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = liblnk_known_folder_location_read_data(
	          known_folder_location,
	          NULL,
	          28,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	LNK_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = liblnk_known_folder_location_read_data(
	          known_folder_location,
	          lnk_test_known_folder_location_data1,
	          (size_t) SSIZE_MAX + 1,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	LNK_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

	result = liblnk_known_folder_location_read_data(
	          known_folder_location,
	          lnk_test_known_folder_location_data1,
	          0,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 -1 );

	LNK_TEST_ASSERT_IS_NOT_NULL(
	 "error",
	 error );

	libcerror_error_free(
	 &error );

#if defined( HAVE_LNK_TEST_MEMORY )

	/* Test liblnk_known_folder_location_read_data with memcpy failing
	 */
	lnk_test_memcpy_attempts_before_fail = 0;

	result = liblnk_known_folder_location_read_data(
	          known_folder_location,
	          lnk_test_known_folder_location_data1,
	          28,
	          &error );

	if( lnk_test_memcpy_attempts_before_fail != -1 )
	{
		lnk_test_memcpy_attempts_before_fail = -1;
	}
	else
	{
		LNK_TEST_ASSERT_EQUAL_INT(
		 "result",
		 result,
		 -1 );

		LNK_TEST_ASSERT_IS_NOT_NULL(
		 "error",
		 error );

		libcerror_error_free(
		 &error );
	}
#endif /* defined( HAVE_LNK_TEST_MEMORY ) */

	/* Clean up
	 */
	result = liblnk_known_folder_location_free(
	          &known_folder_location,
	          &error );

	LNK_TEST_ASSERT_EQUAL_INT(
	 "result",
	 result,
	 1 );

	LNK_TEST_ASSERT_IS_NULL(
	 "known_folder_location",
	 known_folder_location );

	LNK_TEST_ASSERT_IS_NULL(
	 "error",
	 error );

	return( 1 );

on_error:
	if( error != NULL )
	{
		libcerror_error_free(
		 &error );
	}
	if( known_folder_location != NULL )
	{
		liblnk_known_folder_location_free(
		 &known_folder_location,
		 NULL );
	}
	return( 0 );
}

#endif /* defined( __GNUC__ ) && !defined( LIBLNK_DLL_IMPORT ) */

/* The main program
 */
#if defined( HAVE_WIDE_SYSTEM_CHARACTER )
int wmain(
     int argc LNK_TEST_ATTRIBUTE_UNUSED,
     wchar_t * const argv[] LNK_TEST_ATTRIBUTE_UNUSED )
#else
int main(
     int argc LNK_TEST_ATTRIBUTE_UNUSED,
     char * const argv[] LNK_TEST_ATTRIBUTE_UNUSED )
#endif
{
	LNK_TEST_UNREFERENCED_PARAMETER( argc )
	LNK_TEST_UNREFERENCED_PARAMETER( argv )

#if defined( __GNUC__ ) && !defined( LIBLNK_DLL_IMPORT )

	LNK_TEST_RUN(
	 "liblnk_known_folder_location_initialize",
	 lnk_test_known_folder_location_initialize );

	LNK_TEST_RUN(
	 "liblnk_known_folder_location_free",
	 lnk_test_known_folder_location_free );

	LNK_TEST_RUN(
	 "liblnk_known_folder_location_read_data_block",
	 lnk_test_known_folder_location_read_data_block );

	LNK_TEST_RUN(
	 "liblnk_known_folder_location_read_data",
	 lnk_test_known_folder_location_read_data );

#endif /* defined( __GNUC__ ) && !defined( LIBLNK_DLL_IMPORT ) */

	return( EXIT_SUCCESS );

on_error:
	return( EXIT_FAILURE );
}

