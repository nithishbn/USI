package Proteomics::Spectra::UniversalSpectrumIdentifier;

###############################################################################
# Class       : Proteomics::Spectra::UniversalSpectrumIdentifier
# Author      : Eric Deutsch <edeutsch@systemsbiology.org>
#
# Description : This class implements various methods related to the
#               Universal Spectrum Identifier.
#
###############################################################################

use strict;
use warnings;

use Proteomics::Response qw(processParameters);
use Proteomics::Config;

use vars qw( $CLASS $DEBUG $VERBOSE $TESTONLY );

$CLASS = 'Proteomics::Spectra::UniversalSpectrumIdentifier';
$DEBUG = 0;
$VERBOSE = 0;
$TESTONLY = 0;


###############################################################################
# Constructor
###############################################################################
sub new {
  my $METHOD = 'new';
  print "DEBUG: Entering $CLASS.$METHOD\n" if ($DEBUG);
  my $self = shift;
  my %parameters = @_;
  my $class = ref($self) || $self;

  #### Create the object with any default attributes
  $self = {
  };
  bless $self => $class;

  #### Initialize class variables the first time the class is used
  # none

  #### Process constructor argument class variables
  # none

  #### Process constructor object parameters
  my $usi = processParameters( parameters=>\%parameters, caller=>$METHOD, name=>'usi', required=>0, allowUndef=>1 );
  if ( defined($usi) ) {
    $self->setUSI($usi);
  }
  
  #### Complain about any unexpected parameters
  my $unexpectedParameters = '';
  foreach my $parameter ( keys(%parameters) ) { $unexpectedParameters .= "ERROR: unexpected parameter '$parameter'\n"; }
  die("CALLING ERROR [$METHOD]: $unexpectedParameters") if ($unexpectedParameters);

  print "DEBUG: Exiting $CLASS.$METHOD\n" if ( $DEBUG );
  return($self);
}


###############################################################################
# setDEBUG
###############################################################################
sub setDEBUG {
  my $METHOD = "setDEBUG";
  print "DEBUG: Entering $CLASS.$METHOD\n" if ($DEBUG);
  my $self = shift || die("parameter self not passed");
  my $value = shift;
  die("ERROR [$METHOD]: value not passed to $METHOD") if (!defined($value));

  $DEBUG = $value;
  print "DEBUG: Exiting $CLASS.$METHOD\n" if ( $DEBUG );
  return $value;
}


###############################################################################
# setAttribute
###############################################################################
sub setAttribute {
  my $METHOD = 'setAttribute';
  print "DEBUG: Entering $CLASS.$METHOD\n" if ($DEBUG);
  my $self = shift || die("parameter self not passed");
  my $value = shift;
  die("ERROR [$METHOD]: value not passed to $METHOD") if (!defined($value));

  $self->{attribute} = $value;
  print "DEBUG: Exiting $CLASS.$METHOD\n" if ( $DEBUG );
  return;
}


###############################################################################
# setUSI
###############################################################################
sub setUSI {
  my $METHOD = 'setUSI';
  print "DEBUG: Entering $CLASS.$METHOD\n" if ($DEBUG);
  my $self = shift || die("parameter self not passed");
  my $value = shift;
  die("ERROR [$METHOD]: value not passed to $METHOD") if (!defined($value));

  $self->{usi} = $value;
  print "DEBUG: Exiting $CLASS.$METHOD\n" if ( $DEBUG );
  return;
}


###############################################################################
# getLibrary
###############################################################################
sub getLibrary {
  my $METHOD = 'getLibrary';
  print "DEBUG: Entering $CLASS.$METHOD\n" if ($DEBUG);
  my $self = shift || die("parameter self not passed");

  print "DEBUG: Exiting $CLASS.$METHOD\n" if ( $DEBUG );
  return($self->{attribute});
}


###############################################################################
# parse
###############################################################################
sub parse {
  my $METHOD = 'parse';
  print "DEBUG: Entering $CLASS.$METHOD\n" if ( $DEBUG );
  my $self = shift || die ("self not passed");
  my %parameters = @_;

  #### Set up a response object
  my $response = Proteomics::Response->new();

  #### Process standard parameters
  my $debug = processParameters( name=>'debug', required=>0, allowUndef=>0, default=>0, overrideIfFalse=>$DEBUG, parameters=>\%parameters, caller=>$METHOD, response=>$response );
  my $verbose = processParameters( name=>'verbose', required=>0, allowUndef=>0, default=>0, overrideIfFalse=>$VERBOSE, parameters=>\%parameters, caller=>$METHOD, response=>$response );
  my $quiet = processParameters( name=>'quiet', required=>0, allowUndef=>0, default=>0, parameters=>\%parameters, caller=>$METHOD, response=>$response );
  my $outputDestination = processParameters( name=>'outputDestination', required=>0, allowUndef=>0, default=>'STDERR', parameters=>\%parameters, caller=>$METHOD, response=>$response );
  print "DEBUG: Entering $CLASS.$METHOD\n" if ( $debug && !$DEBUG );

  #### Process specific parameters
  my $usi = processParameters( name=>'usi', required=>0, allowUndef=>0, parameters=>\%parameters, caller=>$METHOD, response=>$response );

  #### Die if any unexpected parameters are passed
  my $unexpectedParameters = '';
  foreach my $parameter ( keys(%parameters) ) { $unexpectedParameters .= "ERROR: unexpected parameter '$parameter'\n"; }
  die("CALLING ERROR [$METHOD]: $unexpectedParameters") if ($unexpectedParameters);

  #### Return if there was a problem with the required parameters
  return $response if ( $response->{errorCode} =~ /MissingParameter/i );

  
  #### If the USI is supplied, then store it
  if ( $usi ) {
    $self->setUSI( $usi );

  #### Otherwise, fetch it from the where it was hopefully previously stored or fail
  } else {
    $usi = $self->{usi};
	unless ( $usi ) {
      $response->logEvent( status=>'ERROR', level=>'ERROR', errorCode=>'NoUSI', verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
        message=>"No USI is available to parse");
      return $response;
	}
  }

  #### Parse off the preamble
  if ( $usi =~ /^mzspec:/ ) {
	$usi =~ s/^mzspec://;

  #### Or fail if it's not there
  } else {
	$response->logEvent( status=>'ERROR', level=>'ERROR', errorCode=>'MissingPreamble', verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
      message=>"USI does not begin with expected preamble 'mzspec:'");
    return $response;
  }

  #### Split the rest of the fields
  my @elements = split(":",$usi);
  my $nElements = scalar(@elements);
  my $elementOffset = 0;
  my $offset = 0;

  #### Announce the plan
  $response->logEvent( level=>'INFO', minimumVerbosity=>1, verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
    message=>"Parsing $nElements element USI '$usi'");

  #### Check that there are at least four fields there
  if ( $nElements < 4 ) {
	$response->logEvent( status=>'ERROR', level=>'ERROR', errorCode=>'TooFewFields', verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
      message=>"USI does not have the minimum required 4 colon-separated fields after mzspec:");
    return $response;
  }

  #### Check the dataset identifier field
  $offset = $elementOffset;
  my $datasetIdentifier = $elements[$offset];
  if ( ! $datasetIdentifier ) {
	$response->logEvent( level=>'ERROR', errorCode=>'UndefinedIdentifier', verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
      message=>"Field $elementOffset is empty, which is not permitted");
  } elsif ( $datasetIdentifier =~ /^PXD[\d\.]+$/ ) {
    $response->logEvent( level=>'INFO', minimumVerbosity=>1, verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
      message=>"Field $elementOffset is a well-formed PXD identifier '$datasetIdentifier'");
  } else {
	$response->logEvent( status=>'ERROR', level=>'ERROR', errorCode=>'UnrecognizedIdentifierFormat', verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
      message=>"Identifier '$datasetIdentifier' does not conform to a known allowable identifier, currently only PXDnnnnnn");
  }

  #### Check the next field to see if it is old style
  my $datasetSubfolder = "";
  $elementOffset++;
  $offset = $elementOffset;
  my $nextField = $elements[$offset];
  my $offsetShift = 0;
  if ( $nextField eq '' ) {
    $response->logEvent( level=>'INFO', minimumVerbosity=>1, verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
      message=>"Field $elementOffset is empty, which is consistent with an early style. Assuming it is an empty datasetSubfolder field");
    $offsetShift = 1;
  }


  #### Check the MS run field
  $offset = $elementOffset+$offsetShift;
  my $msRunName = $elements[$offset];
  if ( $msRunName ) {
    $response->logEvent( level=>'INFO', minimumVerbosity=>1, verbose=>$verbose, debug=>$debug, quiet=>$quiet,
      message=>"Field $offset is an MS run name '$msRunName'");
  } else {
    $response->logEvent( status=>'ERROR', level=>'ERROR', errorCode=>'EmptyMsRun', verbose=>$verbose, debug=>$debug, quiet=>$quiet,
      message=>"Field $offset is empty, which is not permitted. It should be an MS Run identifier");
  }

  #### Check the index type field
  $elementOffset++;
  $offset = $elementOffset+$offsetShift;
  my $indexFlag = $elements[$offset];
  if ( $indexFlag ) {
    if ( $indexFlag eq 'scan' || $indexFlag eq 'mgfi' ) {
      $response->logEvent( level=>'INFO', minimumVerbosity=>1, verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
        message=>"Field $offset is index flag '$indexFlag', which is recognized and allowed");

    #### If it is something else, consider the possibility that the MS Run has a colon in it and a valid indexType comes later
    } else {
      my $potentialOffsetShift = $offsetShift;
      my $appendStr = "";
      my $repaired = 0;
      while ( $elementOffset + $potentialOffsetShift <= $nElements ) {
        if ( $elements[$elementOffset + $potentialOffsetShift] =~ /(scan|mgfi)/i ) {
          $indexFlag = $elements[$elementOffset + $potentialOffsetShift];
          $msRunName .= $appendStr;
          $offsetShift = $potentialOffsetShift;
          $repaired++;
          last;
        }
        $appendStr .= ":".$elements[$elementOffset + $potentialOffsetShift];
        $potentialOffsetShift++;
      }
      if ( $repaired ) {
        $response->logEvent( level=>'INFO', minimumVerbosity=>1, verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
          message=>"There appears to be an unescaped colon in the msRun name. This is not good, but has been successfully handled. I hope. Revised msRunName='$msRunName' and indexFlag='$indexFlag'");
      } else {
        $response->logEvent( status=>'ERROR', level=>'ERROR', errorCode=>'UnrecognizedIndexFlag', verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
          message=>"Field $offset is supposed to be an index type (permitted: 'scan' or 'mgfi'), but its value is '$indexFlag'");
      }
    }
  } else {
    $response->logEvent( status=>'ERROR', level=>'ERROR', errorCode=>'EmptyIndexFlag', verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
      message=>"Field $offset index flag is empty, which is not permitted");
  }

  #### Check the index field
  $elementOffset++;
  $offset = $elementOffset+$offsetShift;
  my $index = $elements[$offset];
  if ( defined($index) ) {
    $response->logEvent( level=>'INFO', minimumVerbosity=>1, verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
      message=>"Field $offset is index '$index'");
  } else {
    $response->logEvent( status=>'ERROR', level=>'ERROR', errorCode=>'EmptyIndex', verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
      message=>"Field $offset index is empty, which is not permitted");
  }

  #### Check the interpretation field
  $elementOffset++;
  $offset = $elementOffset+$offsetShift;
  my $interpretation = $elements[$offset];
  my $peptidoform = '';
  my $charge = '';
  if ( defined($interpretation) && $interpretation ne '' ) {
    $response->logEvent( level=>'INFO', minimumVerbosity=>1, verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
      message=>"Field $offset is interpretation '$interpretation'");
    if ( $interpretation =~ /^\s*(.+)\/(\d+)\s*$/ ) {
      $peptidoform = $1;
      $charge = $2;
      $response->logEvent( level=>'INFO', minimumVerbosity=>1, verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
        message=>"Interpreted peptidoform=$peptidoform, charge=$charge");
    } else {
      $response->logEvent( status=>'ERROR', level=>'ERROR', errorCode=>'MalformedInterpretation', verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
        message=>"Unable to parse interpretation '$interpretation' as peptidoform/charge");
    }
  } else {
    $response->logEvent( level=>'INFO', minimumVerbosity=>1, verbose=>$verbose, debug=>$debug, quiet=>$quiet, outputDestination=>$outputDestination, 
      message=>"Field $offset interpretation is not provided, which is okay");
  }

  #### Store the results
  $self->{datasetIdentifier} = $datasetIdentifier;
  $self->{datasetSubfolder} = $datasetSubfolder;
  $self->{msRunName} = $msRunName;
  $self->{indexFlag} = $indexFlag;
  $self->{index} = $index;
  $self->{interpretation} = $interpretation;
  $self->{peptidoform} = $peptidoform;
  $self->{charge} = $charge;

  if ( $response->{nErrors} ) {
    $response->{message} = $response->{errors}->[0];
  }

  print "DEBUG: Exiting $CLASS.$METHOD\n" if ( $debug );
  return $response;
}


###############################################################################
1;
