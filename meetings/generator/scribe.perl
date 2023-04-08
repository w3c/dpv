#!/usr/bin/perl
#
# Converts an IRC log to formatted minutes in HTML.
#
# See scribe2doc.html for the manual.
# This is a rewrite of David Booth's scribe.perl
#
# TODO: option --inputFormat to select the format, rather than try
# each parser in turn.
#
# TODO: Allow (and ignore) the unused options of old scribe.perl?
#
# TODO: Add a command ('oops'? 'undo'? 'ignore'? u///g?) to remove an
# incorrect s///g, because s|s/.../.../g|| doesn't remove it.
#
# TODO: Warn about unrecognized or impossible dates after "Date: ..."
#
# TODO: A streaming mode (using --inputFormat) that formats each line
# as soon as it is read? (s/// and i//// will not work. ScribeNick is
# not retroactive. Broken lines, as in Mirc logs, are not recombined.)
#
# TODO: Make "next meeting" accept a date ("7 Aug") or a period ("in 2
# weeks") and infer a URL?
#
# TODO: If trackbot assigns a number ("ISSUE-3") to an issue, use that
# number instead of the generic "Issue". Also use it in the
# #IssueSummary.
#
# TODO: An option to omit the special handling of W3C's bots
# (currently zakim, rrsagent, agendabot and trackbot).
#
# TODO: Make commands such as scribeoptions:-implicit and
# scribeoptions:-allowspace apply only until they are overridden by
# another?
#
# TODO: RRSAgent has commands to edit or drop actions (because it
# doesn't understand s///). Should we support those?
#
# TODO: An option to add rel=nofollow to links? (In case RRSAgent is
# used to create Google karma for sites.)
#
# TODO: A command to skip several lines or end the minutes before the
# end of the input. ("StopMinutesHere", "ResumeMinutesHere"?)
#
# TODO: Should s/// commands ignore lines by the W3C bots?
#
# TODO: Ivan's minutes generator distinguishes participants (present+)
# from guests (guest+). Should scribe.perl, too?
#
# TODO: Syntax highlighting of verbatim text if there is a language
# indicated after the backquotes (as in GitHub's markdown)? (```java
# ...```)
#
# TODO: Also allow three tildes (~~~) instead of three backquotes, as
# in Markdown?
#
# TODO: A way to include (phrase-level) HTML directly?
#
# TODO: When the minutes don't start with "topic:", the first
# <section> is empty. Remove it.
#
# TODO: A way to indicate that a phrase is in a particular language?
#
# TODO: Add formatting/styling to Zakim's "question" feature?
#
# TODO: Recognize the bots if they joined under another nick name.
#
# Copyright © 2017-2023 World Wide Web Consortium, (Massachusetts Institute
# of Technology, European Research Consortium for Informatics and
# Mathematics, Keio University, Beihang). All Rights Reserved. This
# work is distributed under the W3C® Software License[1] in the hope
# that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.
#
# [1] http://www.w3.org/Consortium/Legal/2015/copyright-software-and-document
# or see the file COPYING included in this distribution.
#
# Created: 3 Feb 2017
# Author: Bert Bos <bert@w3.org>


# Conversion proceeds in six steps:
#
# 1) Various parsers are tried to convert the lines of the input
# into an array of records (see below for the structure of the
# records).
#
# 2) Processing of "s/old/new/" and "i/where/what/" commands.
#
# 3) Scanning for embedded scribeOptions, as they may affect the parsing.
#
# 4) Finding the initial scribe, from a command line option or by
# scanning for the first scribe/scribenick command.
#
# 5) Each record is interpreted, looking for topics, present & regrets,
# actions, resolutions, scribes, statements or summaries minuted by
# the scribes, and remarks by other people on IRC. Each record is
# modified and classified accordingly.
#
# 6) The array of records is converted to an HTML fragment and that
# fragment, together with the collected topics, actions, etc. are
# inserted into an HTML template and printed.
#
# Each record has four fields: {type, speaker, id, text}
# If type is 'i' (irc), <speaker> is the person who typed <text>.
# If type is 'I' (irc), <speaker> is the person who typed verbatim <text>.
# If type is 's' (scribe), <speaker> is the person who said <text> on the phone.
# If type is 'd' (description) <text> is a summary by the scribe.
# If type is 'D' (description) <text> is verbatim text by the scribe.
# If type is 'slideset', <text> is the IRC-formatted link to the slideset
# If type is 'slide', <text> is the number of the slide in the slideset and <id> is the link to the individual slide
# If type is 't' (topic), <text> is the title for a new topic.
# If type is 'T' (subtopic), <text> is the title for a new subtopic.
# If type is 'a' (action), <text> is an action and <id> is a unique ID.
# If type is 'r' (resolution), <text> is a resolution and <id> is a unique ID.
# if type is 'u' (issue), <text> is an issue, <id> a unique ID.
# If type is 'c' (change), the record is a s/// or i/// not (yet) successful
# If type is 'o' (omit), the record is to be ignored.
# If type is 'n' (named anchor), the record is a target anchor.
# If type is 'b' ('bot), the record is info from trackbot.
# If type is 'B' ('bot), <text> is info from trackbot about an issue <id>.
# If type is 'repo', <text> is a list of GitHub repositories.
# If type is 'drop', <text> is a list of GitHub repositories to remove.

use strict;
use warnings;
use Getopt::Long qw(GetOptionsFromString :config auto_version auto_help);
use Pod::Usage;
use v5.16;			# We use "each @ARRAY" (5.012) and fc (5.16)
use locale ':collate';		# Sort using current locale
use utf8;			# This script contains characters in UTF-8
use File::Basename;
use Encode qw/decode/;		# For decode('UTF-8',...)
use Encode::Guess;		# For guess_encoding()
use POSIX 'floor';

# Pattern for URLs. Note: single quote (') does not end a URL.
# The pattern consists of two alternatives. The first one matches a
# URL that is not preceded by a "(" and it allows ")" in the URL. The
# second does not allow ")". This is needed to allow markdown-style
# links, which use "(" and ")" to delimit the URL.
my $urlpat =
  '(?:(?<!\()(?:[a-z]+://|mailto:[^\s<@]+\@|geo:[0-9.]|urn:[a-z0-9-]+:)[^\s<>"‘’“”«»‹›]+|(?:[a-z]+://|mailto:[^\s<@]+\@|geo:[0-9.]|urn:[a-z0-9-]+:)[^\s<>"‘’“”«»‹›)]+)';
# $scribepat is something like "foo" or "foo = John Smith" or "foo/John Smith".
my $scribepat = '([^ ,/=]+) *(?:[=\/] *([^ ,](?:[^,]*[^ ,])?) *)?';
# A speaker name doesn't contain [ ":：>] and doesn't start with "..".
# ("：" is a full-width colon, Unicode U+FF1A.)
my $speakerpat = '(?:[^. :：">]|\\.[^. :：">])[^ :：">]*';
# Some words are unlikely to be speaker names
my $specialpat = '(?:propos(?:ed|al)|issue-\d+|action-\d+|github)';
# A pattern for a GitHub repository.
my $githuburl = '\b(?:(?i)https://github.com/[a-z0-9._-]+/[a-z0-9._-]+)';

# Command line options:
my $styleset = 'public';	# Or 'team', 'member' or 'fancy'
my $embed_diagnostics = 0;	# If 1, put warnings in the HTML, not on STDERR
my $implicitcont = 0;		# If 1, lines without '…' are continuations, too
my $spacecont = 0;		# If 1, initial space may replace '…'
my $keeplines = 1;		# If 1, put <br> between continuation lines
my $final = 0;                  # If 1, don't include "DRAFT" warning in minutes
my $scribenick;			# Nick of the current scribe in lowercase
my $dash_topics = 0;		# If 1, "--" means the next line is a topic
my $use_zakim = 1;		# If 1, treat conversations with Zakim specially
my $scribeonly = 0;		# If 1, omit IRC comments by others
my $emphasis = 0;		# If 1, _xxx_, *xxx* and /xxx/ highlight things
my $old_style = 0;		# If 1, use the old (pre-2017) style sheets
my $url_display = 'break';	# How to display in-your-face URLs
my $logo;			# undef = W3C logo; string = HTML fragment
my $collapse_limit = 30;	# Longer participant lists are collapsed
my $stylesheet;			# URL of style sheet, undef = use defaults
my $mathjax =			# undef = no math; string is MathJax URL
  'https://www.w3.org/scripts/MathJax/3/es5/mml-chtml.js';
my $islide =			# String is i-slide library URL
  'https://w3c.github.io/i-slide/i-slide-2.js?selector=a.islide';
my $github = 1;			# If 0, don't make links for GitHub issues
my $ghurlbot = 1;		# If 0, hide conversations with GHURLbot

# Global variables:
my $has_math = 0;		# Set to 1 by to_mathml()
my @diagnostics;		# Collected warnings and other info
my $recordingstart;         	# Time of recording start secs since midnight)
my $recordingend;         	# Time of recording end (secs since midnight)
my @repositories = ();		# List of repo URLs for expanding issue refs

# Each parser takes a reference to an array of text lines (without
# newlines) and a reference to an array of records. It returns 0
# (failed to parse) or 1 (success) and it appends successfully parsed
# lines to the array of records, with {type} set to 'i' and {speaker}
# and {text} set to the text and the nick of the person who typed that
# text. If a line includes a time stamp, the parser converts it to
# seconds since midnight and puts it in {time}.
# It should not try to parse the text futher for actions, resolutions,
# etc.
#
# IRC messages ("X joined channel Y"), private messages,
# and off-the-record text ("/me waves") are omitted.
#
# The parsers are tried in turn until one succeeds, so their order is
# important. E.g., the Plain_Text_Format should probably be towards
# the end.

my @parsers = (\&RRSAgent_text_format, \&Bip_Format, \&Mirc_Text_Format,
	       \&Yahoo_IM_Format, \&Bert_IRSSI_Format, \&Irssi_Format,
	       \&Qwebirc_paste_format, \&IRCCloud_format,
	       \&Quassel_paste_format, \&Plain_Text_Format);


# RRSAgent_text_format -- parse an IRC log as generated by RRSAgent
sub RRSAgent_text_format($$$$)
{
  my ($lines_ref, $records_ref, $nlines_ref, $err_ref) = @_;

  $$nlines_ref = 0;
  foreach (@$lines_ref) {
    $$nlines_ref++;
    $$err_ref = $_;
    if (/^(?:\d\d:\d\d:\d\d )?<([^ >]+)> \1 has (?:joined|left|changed the topic to:) /) {
      # Ignore lines like "<jfm> jfm has joined #foo"
    } elsif (/^(\d\d):(\d\d):(\d\d) <([^ >]+)> (.*)/) {
      push(@$records_ref, {type=>'i', speaker=>$4, text=>$5,
			   time=> 3600 * $1 + 60 * $2 + $3});
    } elsif (/^<([^ >]+)> (.*)/) {
      push(@$records_ref, {type=>'i', speaker=>$1, text=>$2});
    } elsif (/^\s*$/) {
      # Ignore empty lines
    } else {
      return 0;			# Unknown format, give up
    }
  }
  return 1;
}


# Bip_Format -- parse an IRC log generated by bip
sub Bip_Format($$$$)
{
  my ($lines_ref, $records_ref, $nlines_ref, $err_ref) = @_;

  $$nlines_ref = 0;
  foreach (@$lines_ref) {
    $$nlines_ref++;
    $$err_ref = $_;
    if (/^\d\d-\d\d-\d{4} \d\d:\d\d:\d\d -!- /) {
      # IRC server message, ignore
    } elsif (/^\d\d-\d\d-\d{4} \d\d:\d\d:\d\d [<>] \* /) {
      # /me message, ignore
    } elsif (/^\d\d-\d\d-\d{4} (\d\d):(\d\d):(\d\d) < ([^ !:]+)![^ :]+: (.*)$/){
      push(@$records_ref, {type=>'i', speaker=>$4, text=>$5,
			   time=> 3600 * $1 + 60 * $2 + $3});
    } elsif (/^\d\d-\d\d-\d{4} (\d\d):(\d\d):(\d\d) > ([^ :]+): (.*)$/) {
      push(@$records_ref, {type=>'i', speaker=>$4, text=>$5,
			   time=> 3600 * $1 + 60 * $2 + $3});
    } elsif (/^\s*$/) {
      # Ignore empty lines
    } else {
      return 0;			# Unrecognized line, return failure
    }
  }
  return 1;
}


# Mirc_Text_Format -- log format from saving a MIRC buffer
sub Mirc_Text_Format($$$$)
{
  my ($lines_ref, $records_ref, $nlines_ref, $err_ref) = @_;

  $$nlines_ref = 0;
  foreach (@$lines_ref) {
    $$nlines_ref++;
    $$err_ref = $_;
    if (/^\s*$/) {
      # Empty line, ignore
    } elsif (/^Start of \S+ buffer/) {
      # Skip this (should be first line)
    } elsif (/^End of \S+ buffer/) {
      # Skip this (should be last line)
    } elsif (/^\s*\*/) {
      # Skip /me lines
    } elsif (/^<([^ >]+)> (.*)$/) {
      push(@$records_ref, {type=>'i', speaker=>$1, text=>$2});
    } elsif (/^( .*)$/ && @$records_ref) {	# Continuation line
      $$records_ref[@$records_ref-1]->{text} .= $1;
    } else {
      return 0;			# Unknown format
    }
  }
  return 1;
}


# Yahoo_IM_Format -- saved log from a Yahoo IM session
sub Yahoo_IM_Format($$$$)
{
  my ($lines_ref, $records_ref, $nlines_ref, $err_ref) = @_;

  $$nlines_ref = 0;
  foreach (@$lines_ref) {
    $$nlines_ref++;
    $$err_ref = $_;
    if (/^([^ :]+): (.*)$/) {
      push(@$records_ref, {type=>'i', speaker=>$1, text=>$2});
    } elsif (/^\s*$/) {
      # Ignore empty lines
    } else {
      return 0;
    }
  }
  return 1;
}


# Bert_IRSSI_Format - Bert's IRSSI theme, based on elho, which should also work
sub Bert_IRSSI_Format($$$$)
{
  my ($lines_ref, $records_ref, $nlines_ref, $err_ref) = @_;

  $$nlines_ref = 0;
  foreach (@$lines_ref) {
    $$nlines_ref++;
    $$err_ref = $_;
    next if /^---/;		# IRSSI comment about logging start/stop
    next if /^[0-9:]+\s*[<>-]+ \| (\S+).*( has (?:joined|left).*)/;
    next if /^[0-9:]+\s*«Quit» \| (\S+).* has signed off/;
    next if /^[0-9:]+\s*«[^»]+» \|/; # IRSSI comment about users, topic, etc.
    next if /^[0-9:]+\s*\* \|/;      # Skip a /me command
    next if /^\s*$/;		     # Skip empty line
    if (/^(?:\w\w\w\d\d )?\[?(\d\d):(\d\d)\]?[\s@+%]*(\S+) \| (.*)/) {
      push(@$records_ref, {type=>'i', speaker=>$3, text=>$4,
			   time=> 3600 * $1 + 60 * $2});
    } else {
      return 0;
    }
  }
  return 1;
}


# Irssi_Format - logs from Coralie's Irssi
sub Irssi_Format($$$$)
{
  my ($lines_ref, $records_ref, $nlines_ref, $err_ref) = @_;

  $$nlines_ref = 0;
  foreach (@$lines_ref) {
    $$nlines_ref++;
    $$err_ref = $_;
    next if /^---/;		 # IRSSI comment about logging start/stop
    next if /^[0-9:TZ-]+\s+-!-/; # Skip join/leave and other info
    next if /^[0-9:TZ-]+\s+\*/;	 # Skip a /me command
    next if /^\s*$/;		 # Skip empty line
    if (/^[0-9-]+T(\d\d):(\d\d):(\d\d)Z\s+<([^>]+)> (.*)/) {
      push(@$records_ref, {type=>'i', speaker=>$4, text=>$5,
			   time=> 3600 * $1 + 60 * $2 + $3});
    } else {
      return 0;
    }
  }
  return 1;
}


# Qwebirc_paste_format -- copy-paste from the qwebirc web-based client
sub Qwebirc_paste_format($$$$)
{
  my ($lines_ref, $records_ref, $nlines_ref, $err_ref) = @_;

  $$nlines_ref = 0;
  foreach (@$lines_ref) {
    $$nlines_ref++;
    $$err_ref = $_;
    next if /^\[[0-9:]+\] ==/;	# Join, quit, change nick, change topic, mode
    next if /^\[[0-9:]+\] \*/;	# A message with /me
    next if /^\s*$/;		# Empty line
    if (/^\[(\d\d):(\d\d)\] <([^>]+)> (.*)$/) {
      push @$records_ref, {type=>'i', speaker=>$3, text=>$4,
			   time=> 3600 * $1 + 60 * $2};
    } else {
      return 0;			# This is not qwebirc
    }
  }
  return 1;
}


# IRCCloud_format - the log format of the IRCCloud web service
sub IRCCloud_format($$$$)
{
  my ($lines_ref, $records_ref, $nlines_ref, $err_ref) = @_;

  $$nlines_ref = 0;
  foreach (@$lines_ref) {
    $$nlines_ref++;
    $$err_ref = $_;
    next if /^#[^ ]+$/;				# IRC channel name
    next if /^\[[0-9 :-]+\] → Joined /;	# IRCCloud joined the channel
    next if /^\[[0-9 :-]+\] → [^ ]+ joined /;	# Somebody joined the channel
    next if /^\[[0-9 :-]+\] ⇐ [^ ]+ quit /;	# Somebody disconnected
    next if /^\[[0-9 :-]+\] ⇐ You disconnected/; # User left IRCCloud
    next if /^\[[0-9 :-]+\] ← [^ ]+ left /;	# Somebody left the channel
    next if /^\[[0-9 :-]+\] — [^ ]+ /;		# A /me line
    next if /^\[[0-9 :-]+\] \* [^ ]+ /;		# Changed nick, changed mode...
    if (/^\[[0-9-]+ (\d\d):(\d\d):(\d\d)\] <([^>]+)> (.*)$/) { # $4 said $5
      push @$records_ref, {type=>'i', speaker=>$4, text=>$5,
			   time=> 3600 * $1 + 60 * $2 + $3};
    } else {
      return 0;					# Not an IRCCloud log line
    }
  }
  return 1;					# All lines recognized
}


# Quassel_paste_format -- copy-paste from the Quassel chat window
sub Quassel_paste_format($$$$)
{
  my ($lines_ref, $records_ref, $nlines_ref, $err_ref) = @_;

  # In fact, the date and time between the square brackets can be
  # anything, including month names and arbitrary punctuation. We only
  # look for hh:mm and hh:mm:ss, with or without pm.
  #
  $$nlines_ref = 0;
  foreach (@$lines_ref) {
    $$nlines_ref++;
    $$err_ref = $_;
    next if /^\[.*?\] -->/;		# Somebody joined the channel
    next if /^\[.*?\] <--/;		# Somebody quit the channel
    next if /^\[.*?\] <->/;		# Somebody changed nick
    next if /^\[.*?\] \* /;		# Change of topic, channel created...
    next if /^\[.*?\] -\*-/;		# Somebody used /me
    next if /^\[.*?\] \*\*\*/;		# Channel mode change
    next if /^\[.*?\] - \{/;		# Message "Day changed to ..."
    next if /^\s*$/;			# Skip empty line
    if (/^\[[^]]*(\d\d?):(\d\d)(?::(\d\d))?\s*pm[^]]*\] <([^>]+)> (.*)$/i) {
      push @$records_ref, {type=>'i', speaker=>$4, text=>$5,
			   time=> 3600 * $1 + 60 * (12 + $2) + ($3 // 0)};
    } elsif (/^\[[^]]*(\d\d?):(\d\d)(?::(\d\d))?[^]]*\] <([^>]+)> (.*)$/){
      push @$records_ref, {type=>'i', speaker=>$4, text=>$5,
			   time=> 3600 * $1 + 60 * $2 + ($3 // 0)};
    } elsif (/^\[.*?\] <([^>]+)> (.*)$/) {
      push @$records_ref, {type=>'i', speaker=>$1, text=>$2};
    } else {
      return 0;
    }
  }
  return 1;
}


# Plain_Text_Format -- a simple text format as a scribe might write in an editor
sub Plain_Text_Format($$$$)
{
  my ($lines_ref, $records_ref, $nlines_ref, $err_ref) = @_;

  # This format is meant for taking minutes without IRC. Example:
  #
  #     Topic: Closing issues
  #     Jim: I want to talk about issue 1.
  #     ... And 2, if possible.
  #     [General agreeement]
  #
  # Lines should not start with dates or times, or with bracketed
  # nicknames ("<...>"), as in typical IRC logs. E.g., the following
  # lines cause the parser to conclude that the input is *not*
  # Plain_Text_Format:
  #
  # *   09:34:14 <Sue> Topic: next meeting
  # *   2007-04-04 10:50 Jim: +1
  # *   <Aude> Not now.
  #
  $$nlines_ref = 0;
  foreach (@$lines_ref) {
    $$nlines_ref++;
    $$err_ref = $_;
    return 0 if /^[0-9:-]+[:-][0-9:-]/;		# Seems to start w/ a date/time
    return 0 if /^<[^ >]+> /;			# Seems to start with a <nick>
    if (/^(.+)$/) {				# Not empty
      push (@$records_ref, {type=>'i', speaker=>'scribe', text=>$1});
    }
  }
  return 1;
}


# fc_uniq -- return the list of case-insensitively distinct strings in a list
sub fc_uniq(@)
{
  my %seen;
  return grep {!$seen{fc $_}++} @_;
}


# repository_to_url -- expand a repository name to a full URL, or undef
sub repository_to_url($)
{
  my ($repo) = @_;

  # A full repository URL is "BASE_URL/OWNER/REPO". If BASE_URL is
  # missing, use the one from the previous repo in the list, or
  # https://github.com/. If OWNER is missing, use the one from the
  # previous repo, or "w3c".
  #
  return $repositories[0] if ! $repo; # First repo or undef

  my ($base, $owner, $name) = $repo =~
      /^([a-z]+:\/\/(?:[^\/?#]*\/)*?)?([^\/?#]+\/)?([^\/?#]+)\/?$/i;

  return "$base$owner$name" if $base;	# Just omit the final /, if any
  return @repositories ? $repositories[0] =~ s/[^\/]+\/[^\/]+$/$owner$name/r :
      "https://github.com/$owner$name" if $owner;
  return undef if ! $name;	# Malformed repo name
  return "https://github.com/w3c/$name" if ! @repositories; # Assume w3c
  return $repositories[0] =~ s/[^\/]+$/$name/r;	# Copy base/owner from previous
}


# to_mathml -- call latexmlmath to convert a LaTeX math expression to MathML
sub to_mathml($)
{
  my ($s) = @_;
  my ($in, $out);
  $in = $s;
  $in =~ s/\\/\\\\/g;
  $in =~ s/\"/\\\"/g;
  $in =~ s/\$/\\\$/g;
  $in =~ s/\`/\\\`/g;
  # $out = `latexmlmath "$in" 2>/dev/null`;
  $out = decode('UTF-8', `latexmlmath "$in" 2>/dev/null`);
  push(@diagnostics, "Failed math formula: $s") if $? != 0;
  return $s if $? != 0;		# An error occurred, return original string
  $out =~ s/<\?xml[^>]*\?>\n?//;
  $has_math = 1;
  return $out;
}


{
  my %tag = ('_' => 'u', '/' => 'em', '*' => 'strong', '`' => 'code');

  # to_emph -- replace emphasis marks and math
  sub to_emph($);
  sub to_emph($)
  {
    # Note: $` and $' must be stored in local variables before the
    # recursive call, because they are global variables and might be
    # changed in that call.
    #
    for ($_[0]) {
      if (m{(?:^|\s|\p{P})\K([_/*`])(.+?)\g{1}(?=\p{P}|\s|$)}) {
	my ($a, $z, $t, $m) = ($`, $', $1, $2);
	return to_emph($a)."<$tag{$t}>".to_emph($m)."</$tag{$t}>".to_emph($z);
      } elsif (/(?:^|[^\\])\K\$\$[^\$]+\$\$/) { # $$...$$ not preceded by a '\'
	my ($a, $m, $z) = ($`, $&, $');
	return to_emph($a) . to_mathml($m) . to_emph($z);
      } elsif (/(?:^|[^\\])\K\$[^\$]+\$/) {	# $...$ not preceded by a '\'
	my ($a, $m, $z) = ($`, $&, $');
	return to_emph($a) . to_mathml($m) . to_emph($z);
      } elsif (/\\\$/) {			# Escaped $
	my ($a, $z) = ($`, $');
	return to_emph($a) . '$' . to_emph($z);
      } else {
	return $_;
      }
    }
  }
}


# break_url -- apply -urlDisplay option to a URL
sub break_url($)
{
  my ($s) = @_;

  # HTML delimiters are already escaped.

  # If the URL is a well-known one, replace it with an
  # abbreviation. Otherwise, if the urlDisplay option is 'break',
  # insert <wbr> tags to make the URL breakable. Otherwise, if the
  # urlDisplay option is 'shorten', elide the middle part of the
  # URL. Otherwise return the URL unchanged.
  return "$1/<wbr>$2"
      if $s =~ /^https:\/\/github.com\/([^\/]+)\/([^\/]+)\/?$/;
  return "$1/<wbr>$2#$4"
      if $s =~ /^https:\/\/github.com\/([^\/]+)\/([^\/]+)\/(issues|pull)\/([0-9]+)$/;
  return "$1/<wbr>$2#$4 (comment)"
      if $s =~ /^https:\/\/github.com\/([^\/]+)\/([^\/]+)\/(issues|pull)\/([0-9]+)#issuecomment-/;
  return $s =~ s|/\b|/<wbr>|gr
      if $url_display eq 'break';
  return $s =~ s/^((?:[^&]|&[^;]+;){5})(?:[^&]|&[^;]+;)*((?:[^&]|&[^;]+;){6})$/$1…$2/r
      if $url_display eq 'shorten';
  return $s;
}


# mklink -- return HTML for a URL with anchortext: link, image or just text
sub mklink($$$$)
{
  my ($link, $type, $url, $anchortext) = @_;
  # $link determines whether to make a link (>0) or just show the text (<0).
  # $type determines whether to make a text ("->") or an image ("-->").

  $url = esc($url);
  if ($link > 0) {
    my $s = '<a href="' . $url . '">';
    if ($type eq '-->') {
      $s .= '<img src="' . $url . '" alt="' . esc($anchortext) . '">';
    } elsif ($anchortext ne '') {
      $s .= esc($anchortext, $emphasis);
    } else {
      $s .= break_url($url); # Otherwise the URL itself is the anchor text
    }
    return "$s</a>";
  } else {
    return $anchortext ne '' ? esc($anchortext) : break_url($url);
  }
}


# esc -- escape HTML delimiters (<>&"), optionally handle emphasis & Ralph links
sub esc($;$$$$);
sub esc($;$$$$)
{
  my ($s, $emph, $link, $break_urls, $github) = @_;
  my ($replacement, $pre, $url, $post, $type, $r);

  if ($link) {
    # Wrap Ralph-links and bare URLs in <a>.
    # 1a) A double-quoted Ralph link: ... -> URL "ANCHOR" ...
    # 1b) A single-quoted Ralph link: ... -> URL 'ANCHOR' ...
    # 1a) An unquoted Ralph link: ... -> URL ANCHOR
    # 2) A Xueyuan link: ANCHOR -> URL
    # 3) An Ivan link: ... -> ANCHOR URL ...
    # 4a) A double-quoted inverted Xueyuan link: ... URL -> "ANCHOR" ...
    # 4b) A single-quoted inverted Xueyuan link: ... URL -> 'ANCHOR' ...
    # 4c) An unquoted inverted Xueyuan link: ... URL -> ANCHOR
    # 5) A markdown link: ... [ANCHOR](URL)
    # 6) A bare URL: ... URL ...
    # With --> instead of ->, the link is embedded as an image (<img>).
    # If $link < 0, omit the <a> tag and just insert the text or image.

    # Loop until we found all URLs.
    $replacement = '';
    while (($pre, $url, $post) = $s =~ /^(.*?)($urlpat)(.*)$/i) {
      # Look for "->" or "-->" before or after the URL.
      if ($pre =~ /(--?>) *$/p) { # Ralph, Xueyuan or missing anchor text
	$type = $1;
	$pre = $`;
	if ($post =~ /^ *"([^"\t]*)"/p || $post =~ /^ *'([^'\t]*)'/p ||
	    $post =~ /^ *([^'" \t][^\t]*[^ \t]) */p ||
	    $post =~ /^ *([^'" \t]) */p) { # Ralph link
	  $replacement .= esc($pre, $emph, 0, 0, $github)
	      . mklink($link, $type, $url, $1);
	  $s = $';
	} elsif ($pre =~ / *([^ \t][^\t]*[^ \t]|[^ \t]) *$/p) {	# Xueyuan link
	  $replacement .= esc($`, $emph, 0, 0, $github)
	      . mklink($link, $type, $url,$1);
	  $s = $post;
	} else {		# Missing anchor text
	  $replacement .= esc($pre, $emph, 0, 0, $github)
	      . mklink($link, $type, $url, '');
	  $s = $post;
	}
      } elsif ($pre =~ /(--?>) *(.+?) *$/p) { # Ivan link
	$replacement .= esc($`, $emph, 0, 0, $github)
	    . mklink($link, $1, $url, $2);
	$s = $post;
      } elsif ($post =~ /^ *(--?>) *"([^"\t]*)"/p ||
	       $post =~ /^ *(--?>) *'([^'\t]*)'/p ||
	       $post =~ /^ *(--?>) *([^ \t][^\t]*[^ \t]) */p ||
	       $post =~ /^ *(--?>) *([^ \t]) */p ||
	       $post =~ /^ *(--?>) *()/p) { # Inverted Xueyuan link
	$replacement  .= esc($pre, $emph, 0, 0, $github)
	    . mklink($link, $1, $url, $2);
	$s = $';
      } elsif ($post =~ /^\)/ && $pre =~ /(\[([^\]]+)\]\()$/p) { # Markdown
        $replacement .= esc($`, $emph)
	      . mklink($link, "->", $url, $2);
    	$s = $post =~ s/^\)//r;
      } else {					# Bare URL.
    	$replacement .= esc($pre, $emph, 0, 0, $github)
	    . mklink($link, '->', $url, '');
    	$s = $post;
      }
    }
    $s = $replacement . esc($s, $emph, 0, 0, $github);
  } elsif ($break_urls) {	# Shorten or break URLs
    $s = esc($s, $emph);
    $s =~ s/($urlpat)/break_url($1)/gie;
  } elsif ($github) {
    $replacement = '';
    while ($s =~ /(?:^|\W)\K((?:[a-z0-9._-]+\/)?[a-z0-9._-]+)?#([0-9]+)(?=\W|$)/i) {
     $s = $';
     my ($repo, $issue) = ($1 // '', $2);
     $replacement .= esc($`, $emph);
     $replacement .=  ($r = repository_to_url($repo))
      ? '<a href="'.esc("$r/issues/$issue")."\">$repo#$issue</a>"
      : "$repo#$issue";
    }
    $s = $replacement . esc($s, $emph);
  } else {
    $s =~ s/&/&amp;/g;
    $s =~ s/</&lt;/g;
    $s =~ s/>/&gt;/g;
    $s =~ s/"/&quot;/g;
    if ($emph) {
      $s =~ s/:-\)/☺/g;
      $s =~ s/;-\)/😉\x{FE0E}/g;
      $s =~ s/:-\(/☹/g;
      $s =~ s{:-/}{😕\x{FE0E}}g;
      $s =~ s/,-\)/😜\x{FE0E}/g;
      $s =~ s{\\o/}{🙌\x{FE0E}}g;
      $s =~ s/(?:^|[^-])\K--&gt;/⟶/g;
      $s =~ s/(?:^|[^-])\K-&gt;/→/g;
      $s =~ s/(?:^|[^=])\K==&gt;/⟹/g;
      $s =~ s/(?:^|[^=])\K=&gt;/⇒/g;
      $s =~ s/&lt;--(?!-)/⟵/g;
      $s =~ s/&lt;-(?!-)/←/g;
      $s =~ s/&lt;==(?!=)/⟸/g;
      $s =~ s/&lt;=(?!=)/⇐/g;
      $s = to_emph($s);		# Italics, bold, underline, monospace, math
    }
  }
  return $s;
}


# is_cur_scribe -- true if $nick is in %$curscribes_ref, ignores trailing "_"
sub is_cur_scribe($$)
{
  my ($nick, $curscribes_ref) = @_;

  return $$curscribes_ref{fc($nick =~ s/_+$//r)} || $$curscribes_ref{'*'};
}


# add_scribes -- add scribes to the scribe list and the current scribes
sub add_scribes($$$)
{
  my ($names, $curscribes_ref, $scribes_ref) = @_;

  # We may assume $names matches zero or more comma-separated $scribepat
  foreach (split(/ *, */, $names)) {	# Split at commas
    my ($nick, $real) = /^$scribepat$/;	# Split into nick and real name
    my $n = fc($nick =~ s/_+$//r);	# Case-insensitive, without trailing _
    $$curscribes_ref{$n} = 1;		# Add speaker as scribe
    # Add a new real name, or use the nick as real name if there was none.
    if ($real) {$$scribes_ref{$n} = $real;}
    elsif (!$$scribes_ref{$n}) {$$scribes_ref{$n} = $nick;}
  }
}


# delete_scribes -- remove from current scribe list
sub delete_scribes($$)
{
  my ($names, $curscribes_ref) = @_;

  # We may assume $names matches zero or more comma-separated $scribepat
  foreach (split(/ *, */, $names)) {	# Split at commas
    my ($nick, $real) = /^$scribepat$/;	# Split into name and real name
    my $n = fc($nick =~ s/_+$//r);	# Case-insensitive, without trailing _
    delete $$curscribes_ref{$n};	# Remove from curscribes
  }
}


# link_to_recording -- return an HTML link to the recording at $time, or ""
sub link_to_recording($$)
{
  my ($url, $time) = @_;
  my ($offset, $endoffset);

  return '' if !defined $url || !defined $recordingstart || !defined $time;
  $offset = $time - $recordingstart;
  # If they are more than 8 hours apart, we assume we're comparing
  # across midnight and add 24 hours.
  $offset += 24 * 3600 if $offset < -8 * 3600;
  return '' if $offset < 0;	# We're before the start of the recording

  # Check if we are already after the end of the recording.
  if (defined $recordingend) {
    $endoffset = $recordingend - $time;
    $endoffset += 24 * 3600 if $endoffset < -8 * 3600;
    return '' if $endoffset <= 0;
  }
  return sprintf " <a href=\"%1\$s#t=%2\$s\" class=recording title=\"matching video record\">🎞\x{FE0E}</a>", esc($url), $offset;
}


# add_repositories -- expand repository names to full URLs and remember them
sub add_repositories($)
{
  my $repos = shift;
  my $r;

  # $repos is a comma- or space-separated list of possibly abbreviated
  # repository names. Expand them to full URLs and prefix the
  # resulting list of URLs to the global @repositories. E.g.,
  # "foo/bar, other/bar, baz" is expanded to
  # "https://github.com/foo/bar, https://github.com/other/bar,
  # https://github.com/other/baz".
  #
  foreach (split /[ ,]+/, $repos) {
    if (($r = repository_to_url($_))) {
      unshift @repositories, $r;
    } else {
      push @diagnostics, "Could not interpret as a repository: $_";
    }
  }
}

# remove_repositories -- remove one or more repositories from the list
sub remove_repositories($)
{
  my ($repos) = @_;
  my $r;

  foreach (split /[ ,]+/, $repos) {
    if (($r = repository_to_url($_))) {
      @repositories = grep $_ ne $r, @repositories;
    } else {
      push @diagnostics, "Could not interpret as a repository: $_";
    }
  }
}


# Main body
my $revision = '$Revision: 217 $'
  =~ s/\$Revision: //r
  =~ s/ \$//r;
my $versiondate = '$Date: Fri Apr  7 17:23:01 2023 UTC $'
  =~ s/\$Date: //r
  =~ s/ \$//r;

my %scribes;			# List of scribes
my @records;			# Array of parsed lines
my $date;			# Date of the meeting
my $meeting = "(MEETING TITLE)"; # Name of the meeting (HTML-escaped)
my $prev_meeting = '';		# HTML-formatted link to previous meeting
my $next_meeting = '';		# HTML-formatted link to next meeting
my %present;			# List of participants
my %regrets;			# List of regrets
my $minutes_url;		# URL of the minutes according to RRSAgent
my $logging_url;		# URL of the log according to RRSAgent
my $agenda = '';		# HTML-formatted link to an agenda
my %chairs;			# List of meeting chairs
my %lastspeaker;		# Current speaker (separate for each scribe)
my $speakerid = 's00';		# Generates unique ID for each speaker
my $has_slides = 0;		# Set to 1 if there is at least one slideset
my $lastslideset;		# URL of the slideset being presented
my $recording;         		# URL of the recording of the meeting
my $recording_link;		# HTML-formatted link to the recording
my $topicid = 't00';		# Generates unique ID for each topic
my $actionid = 'a00';		# Generates unique ID for each action
my $resolutionid = 'r00';	# Generates unique ID for each resolution
my $issueid = 'i00';		# Generates unique ID for each issue
my $lineid = 'x000';		# Generates unique ID for each line
my %speakers;			# Unique ID for each speaker
my %namedanchors;		# Set of already used IDs for NamedAnchorsHere
my %curscribes;			# Indexes are the current scribenicks
my %verbatim;			# End of preformatted mode for nick: ``` or ]]
my $agenda_icon = '<img alt="Agenda." title="Agenda" ' .
  'src="https://www.w3.org/StyleSheets/scribe2/chronometer.png">';
my $irclog_icon = '<img alt="IRC log." title="IRC log" ' .
  'src="https://www.w3.org/StyleSheets/scribe2/text-plain.png">';
my $previous_icon = '<img alt="Previous meeting." title="Previous meeting" ' .
  'src="https://www.w3.org/StyleSheets/scribe2/go-previous.png">';
my $next_icon = '<img alt="Next meeting." title="Next meeting" ' .
  'src="https://www.w3.org/StyleSheets/scribe2/go-next.png">';
my $w3clogo = '<a href="https://www.w3.org/"><img src="https://www.w3.org/' .
  'StyleSheets/TR/2016/logos/W3C" alt=W3C border=0 height=48 width=72></a>';

my %bots = (fc('RRSAgent') => 1, # Nicks that probably aren't scribe
	    fc('trackbot') => 1,
	    fc('ghurlbot') => 1,
	    fc('agendabot') => 1,
	    fc('Zakim') => 1);

my %options = ("team" => sub {$styleset = 'team'},
	       "member" => sub {$styleset = 'member'},
	       "fancy" => sub {$styleset = 'fancy'},
	       "embedDiagnostics!" => \$embed_diagnostics,
	       "implicitContinuations!" => \$implicitcont,
	       "allowSpaceContinuation!" => \$spacecont,
	       "keepLines!" => \$keeplines,
	       "urlDisplay=s" => sub {
		 if ($_[1] =~ /^(?:break|shorten|full$)/i) {$url_display=$_[1]}
		 else {die "--urlDisplay must be break, shorten or full\n"}},
	       "final!" => \$final,
	       "draft!" => sub {$final = ! $_[1]},
	       "scribenick=s" => \$scribenick,
	       "dashTopics!" => \$dash_topics,
	       "useZakimTopics!" => \$use_zakim,
	       "scribeOnly!" => \$scribeonly,
	       "emphasis!" => \$emphasis,
	       "mathjax=s" => \$mathjax,
	       "islide=s" => \$islide,
	       "oldStyle!" => \$old_style,
	       "stylesheet:s" => \$stylesheet,
	       "logo:s" => \$logo,
	       "nologo" => sub {$logo = ''},
	       "collapseLimit:i" => \$collapse_limit,
	       "githubIssues!" => \$github,
	       "ghurlbot!" => \$ghurlbot,
	       "minutes=s" => \$minutes_url);
my @month = ('', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
	     'August', 'September', 'October', 'November', 'December');

# Automatically encode output to stdout and stderr as UTF-8. We do not
# automatically decode stdin as UTF-8, because the program might
# occasionally be used on old files that are in Latin-1.
# guess_encoding() below detects that case.
#
binmode(STDOUT, ':utf8');
binmode(STDERR, ':utf8');

GetOptionsFromString($ENV{"SCRIBEOPTIONS"}, %options) if $ENV{"SCRIBEOPTIONS"};
GetOptions(%options) or pod2usage(2);

# Step 1: Read all lines into a temporary array; replace tabs by
# spaces and remove carriage returns and newlines; then try each
# parser in turn to parse them into records, until one succeeds.
#
do {
  local $/;
  my $input = <>;
  # Try to guess the encoding: ASCII, UTF-8/16/32 or Latin-1.
  my $decoder = guess_encoding($input, 'latin-1');
  # Decode the input. If not known or ambiguous, try UTF-8.
  $input = ref($decoder) ? $decoder->decode($input) : decode('UTF-8', $input);
  # Split into lines, remove newlines, replace tabs by spaces.
  my @input = map tr/\t/ /r, split(/\r?\n/, $input);
  $input[0] =~ s/^\x{FEFF}// if scalar @input; # Remove the BOM, if any
  my ($nlines, $errline, $n, $e) = (0, '', 0, '');
  do {
    last if &$_(\@input, \@records, \$n, \$e);
    ($nlines, $errline) = ($n, $e) if $n > $nlines;
    @records = ();
  } foreach (@parsers);
  push(@diagnostics, 'Input is empty.') if !@records && !$nlines;
  push(@diagnostics, "Unrecognized input at line $nlines: $errline")
      if !@records && $nlines;
};

# Step 2: Process s/old/new/ and i/where/what/ commands.
#
# First mark all s/// and i/// lines as 'c', so that they don't get
# changed by other s/// lines. Then loop over all lines again and
# apply the substitutions and insertions. Successful s/// and i///
# become of type 'o' (omit).
#
# If people try to use s/// to replace URLs and they copy-paste the
# URLs from certain old minutes, there might be zero-width non-joiner
# characters in the URLs. Remove them before matching.
#
foreach (@records) {
  $_->{type} = 'c' if
      $_->{text} =~ /^ *(s|i)(\/|\|)(.*?)\2(.*?)(?:\2([gG])?.*)?$/;
}

for (my $i = 0; $i < @records; $i++) {

  if ($records[$i]->{type} eq 'c' &&
      $records[$i]->{text} =~ /^ *(s|i)(\/|\|)(.*?)\2(.*?)(?:\2([gG])?.*)?$/) {
    my ($cmd, $old, $new, $global) = ($1, $3, $4, $5);
    my $old2 = $old =~ s/\x{200C}//gr;		# Version without any U+200C

    if ($cmd eq 'i') {				# i/where/what/
      my $j = $i - 1;
      $j-- until $j < 0 || ($records[$j]->{type} eq 'i' &&
			    ($records[$j]->{text} =~ /\Q$old\E/ ||
			     $records[$j]->{text} =~ /\Q$old2\E/));
      if ($j >= 0) {
	splice(@records, $j, 0,
	       {type=>'i',speaker=>$records[$i]->{speaker},text=>$new});
	$i++;			# All records shifted by the splice
	$records[$i]->{type} = 'o';
	push(@diagnostics, 'Succeeded: ' . $records[$i]->{text});
      } else {
	push(@diagnostics, 'Failed: ' . $records[$i]->{text});
      }

    } elsif (! defined $global) {		# s/old/new/
      my $j = $i - 1;
      $j-- until $j < 0 || ($records[$j]->{type} eq 'i' &&
			    ($records[$j]->{text} =~ s/\Q$old\E/$new/ ||
			     $records[$j]->{text} =~ s/\Q$old2\E/$new/));

      push(@diagnostics,
	   ($j >= 0 ? 'Succeeded: ' : 'Failed: ') . $records[$i]->{text});
      $records[$i]->{type} = 'o' if $j >= 0; # Omit successful command

    } else {					# s/old/new/g or .../G
      my $n = 0;
      for (0 .. ($global eq 'g' ? $i-1 : @records-1)) {
	$n++ if $records[$_]->{type} eq 'i' &&
	    ($records[$_]->{text} =~ s/\Q$old\E/$new/ ||
	     $records[$_]->{text} =~ s/\Q$old2\E/$new/);
      }
      push(@diagnostics,
	   ($n ? "Succeeded $n times: " : "Failed: ") . $records[$i]->{text});
      $records[$i]->{type} = 'o' if $n; # Omit successful command
    }
  }
}

# Step 3: Search for scribeOptions, as they may affect the whole log.
#
foreach my $p (@records) {
  if ($p->{text} =~ /^ *scribeoptions *: *(.*?) *$/i) {
    Getopt::Long::Configure("pass_through");
    my ($ret, $args) = GetOptionsFromString($1, %options);
    push(@diagnostics, 'Unknown option in scribeoptions: ' . join(' ', @$args))
	if scalar @$args;
    $p->{type} = 'o';			# Omit line from output
  }
}

# Step 4: Find the initial scribe(s).
#
# The first scribe/scribenick command is also assumed to apply to the
# lines that come before it, so search for that first command (unless
# --scribenick was given on the command line). If no command is found,
# assume the person who typed most was the scribe. And if nobody typed
# anything, set the scribe to '*'.
#
# The hash %count is also used further down to print the list of
# people who were active on IRC in the diagnostics.
#
my %count;
foreach (@records) {
  $count{$_->{speaker}}++ if $_->{type} eq 'i' && !$bots{fc($_->{speaker})};
}
while (!defined $scribenick && (my ($i,$p) = each @records)) {
  if ($p->{text} =~ /^ *scribe(?:nick)? * \+[:：]? *$/i) {
    $scribenick = $p->{speaker};
  } elsif ($p->{text} =~ /^ *scribe(?:nick)? *(?:[:：]|\+[:：]?) *($scribepat(?:, *$scribepat)*)$/i) {
    $scribenick = $1;
  }
}
if (!defined $scribenick) {
  $scribenick = (sort {$count{$b} <=> $count{$a}} sort keys %count)[0];
  # If still undef, it means there are no lines at all...
  $scribenick = '*' if !defined $scribenick;
  push(@diagnostics, "No scribenick or scribe found. Guessed: $scribenick");
}
add_scribes($scribenick, \%curscribes, \%scribes);

# Step 5: Interpret each record, collect topics, actions, etc.
#
# Interpret each line. %curscribes is the current set of scribes in lowercase.
# $lastspeaker is the current speaker, for use in continuation lines.
# $lastspeaker is set to foo whenever the scribe writes "foo: ...".
#
for (my $i = 0; $i < @records; $i++) {
  my $is_scribe = is_cur_scribe($records[$i]->{speaker}, \%curscribes);
  $_ = $records[$i]->{text};

  if ($records[$i]->{type} eq 'o') {
    # This record was already processed

  } elsif (/^ *$/) {
    $records[$i]->{type} = 'o';		# Omit empty line

  } elsif (/^ *(```|\[\[) *$/ &&	# Start preformatted text
      !exists $verbatim{$records[$i]->{speaker}}) {
    $verbatim{$records[$i]->{speaker}} = $1 eq "```" ? "```" : "]]";
    if ($is_scribe) {
      $records[$i]->{text} = "";	# Next lines will be appended
      $records[$i]->{type} = 'D';	# Preformatted text by scribe
    } else {
      $records[$i]->{type} = 'o';	# Omit this record
    }

  } elsif (/ *(```|\]\]) *$/ &&		# End of preformatted text
      ($verbatim{$records[$i]->{speaker}} // "") eq $1) {
    $records[$i]->{type} = 'o';			# Omit this record
    delete $verbatim{$records[$i]->{speaker}};	# Remove verbatim mode

  } elsif (exists $verbatim{$records[$i]->{speaker}}) { # Preformatted text
    if ($is_scribe) {
      # Scribe's verbatim text is collected into a single record
      my $j = $i - 1;
      $j-- while $records[$j]->{type} eq 'o' ||
	  $records[$j]->{speaker} ne $records[$i]->{speaker};
      $records[$j]->{text} .= $records[$i]->{text} . "\n"; # Append to 1st line
      $records[$i]->{type} = 'o';			   # Omit this record
    } else {
      $records[$i]->{type} = 'I';		# Mark as preformatted line
    }

  } elsif (/^ *present *[:：=] *(.*?) *$/i) {
    if ($records[$i]->{speaker} eq 'Zakim' && !$use_zakim) {} # Ignore Zakim?
    elsif ($1 eq '(no one)') {%present = ()}
    else {%present = map {fc($_) => $_} split(/ *, */, $1)}
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *present *\+[:：]? *$/i) {
    $present{fc $records[$i]->{speaker}} = $records[$i]->{speaker};
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *present *\+[:：]? *(.*?) *$/i) {
    $present{fc $_} = $_ foreach split(/ *, */, $1);
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *present *-[:：]? *(.*?) *$/i) {
    delete $present{fc $_} foreach split(/ *, */, $1);
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *regrets? *[:：] *(.*?) *$/i) {
    %regrets = map { fc($_) => $_ } split(/ *, */, $1);
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *regrets? *\+[:：]? *$/i) {
    $regrets{fc $records[$i]->{speaker}} = $records[$i]->{speaker};
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *regrets? *\+[:：]? *(.*?) *$/i) {
    $regrets{fc $_} = $_ foreach split(/ *, */, $1);
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *regrets? *-[:：]? *(.*?) *$/i) {
    delete $regrets{fc $_} foreach split(/ *, */, $1);
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *repo(?:s|sitory|sitories)? *(?:[:：]|\+[:：]?) *(.*?) *$/i ||
      /^ *ghurlbot *, *(?:discuss(?:ing)?|use|using|take +up|taking +up|this +(?:will +be|is)) +(.*?) *$/i) {
    $records[$i]->{type} = 'repo';	# Mark as repository line
    $records[$i]->{text} = $1;

  } elsif (/^ *repo(?:s|sitory|sitories)? *-[:：]? *(.*?) *$/i ||
    /^ *ghurlbot *, *(?:forget|drop|remove|don't +use|do +not +use) +([^ ]+) *$/i) {
    $records[$i]->{type} = 'drop';	# Mark as drop-repository line
    $records[$i]->{text} = $1;

  } elsif (/^ *slides(?:et)? *[:：] *(.*?($urlpat).*)$/i) {
    $records[$i]->{type} = 'slideset';	# Mark as slideset line
    $records[$i]->{text} = $1;
    $lastslideset = $2;
    $has_slides = 1;

  } elsif (/^ *slideset *[:：]/i) {	# Slideset but without a URL. Error?
    $records[$i]->{type} = 'd' if $is_scribe;
    $lastslideset = undef;

  } elsif (/^ *\[ *slide *(\d+) *\] *$/i && $lastslideset) {
    $records[$i]->{type} = 'slide';	# Mark as slide line
    my $slidenumber = $1;
    # Put link in {id}, with fragment ID "#n" (or #page=n for PDF URLs).
    $records[$i]->{id} = $lastslideset . "#" .
	($lastslideset =~ /\.pdf/ ? "page=" : "") . $slidenumber;
    $records[$i]->{text} = "$slidenumber";

  } elsif (/^ *recording *[:：] *(.*?($urlpat).*)$/i) {
    $records[$i]->{type} = 'o';		# Omit line from output
    $recording_link = esc($1, $emphasis, 1, 1);
    $recording = $2;

  } elsif (/^ *recording *[:：]/i) {	# Recording but without a URL. Error?
    $records[$i]->{type} = 'd' if $is_scribe;
    $recording = undef;

  } elsif (/^ *recording +(?:is +starting|starts)[. ]*$/i) {
    $records[$i]->{type} = 'o';		# Omit line from output
    $recordingstart = $records[$i]->{time} if defined $records[$i]->{time};

  } elsif (/^ *recording +start(?:ed|s) +at +[:：]([0-9][0-9])[. ]*$/i) {
    $records[$i]->{type} = 'o';		# Omit line from output
    $recordingstart = 3600*floor(($records[$i]->{time} - 60*$1)/3600) + 60*$1
	if defined($records[$i]->{time});


  } elsif (/^ *recording +ends[. ]*$/i) {
    $records[$i]->{type} = 'o';		# Omit line from output
    $recordingend = $records[$i]->{time} if defined $records[$i]->{time};

  } elsif (/^ *recording +end(?:ed|s) +at +[:：]([0-9][0-9])[. ]*$/i) {
    $records[$i]->{type} = 'o';		# Omit line from output
    $recordingend = 3600*floor(($records[$i]->{time} - 60*$1)/3600) + 60*$1
	if defined $records[$i]->{time};

  } elsif (/^ *topic *[:：] *(.*?) *$/i) {
    $records[$i]->{type} = 't';		# Mark as topic line
    $records[$i]->{text} = $1;
    $records[$i]->{id} = ++$topicid;	# Unique ID

  } elsif (/^ *sub-?topic *[:：] *(.*?) *$/i) {
    $records[$i]->{type} = 'T';		# Mark as subtopic line
    $records[$i]->{text} = $1;
    $records[$i]->{id} = ++$topicid;	# Unique ID

  } elsif ($dash_topics && /^ *-+ *$/) {
    my $topicfound = 0;
    for (my $j = $i + 1; $j < @records; $j++) {
      if ($records[$j]->{speaker} eq $records[$i]->{speaker}) {
	$records[$i]->{type} = 't';
	$records[$i]->{text} = $records[$j]->{text} =~ s/^ *(.*?) *$/$1/r;
	$records[$i]->{id} = ++$topicid;
	$records[$j]->{type} = 'o';
        $topicfound = 1;
	last;
      }
    }

  } elsif ($records[$i]->{speaker} eq 'RRSAgent' && / to generate ([^ #]+)/) {
    $minutes_url = $1;
    $records[$i]->{type} = 'o';		# Ignore this line

  } elsif ($records[$i]->{speaker} eq 'RRSAgent' &&
	   /(?:[Ll]ogging to|recorded in|See) ([^ #]+)/){
    $logging_url = $1;
    $records[$i]->{type} = 'o';		# Ignore this line

  } elsif (/^ *rrsagent,/i) {
    $records[$i]->{type} = 'o';		# Ignore this line

  } elsif ($records[$i]->{speaker} eq 'RRSAgent') {
    # Ignore RRSAgent's list of actions, etc.
    $records[$i]->{type} = 'o';		# Ignore this line

  } elsif (/^ *action *[:：] *(.*?) *$/i ||
	   /^ *action +(\pL\w* *[:：].*?) *$/i ||
	   /^ *action +([^ ]+ +to\b.*?) *$/i) {
    $records[$i]->{type} = 'a';		# Mark as action line
    $records[$i]->{text} = $1;
    $records[$i]->{id} = ++$actionid;	# Unique ID

  } elsif (/^ *resol(?:ved|ution) *[:：] *(.*?) *$/i) {
    $records[$i]->{type} = 'r';		# Mark as resolution line
    $records[$i]->{text} = $1;
    $records[$i]->{id} = ++$resolutionid;

  } elsif (/^ *issue *[:：] *(.*?) *$/i) {
    $records[$i]->{type} = 'u';		# Mark as issue line
    $records[$i]->{text} = $1;
    $records[$i]->{id} = ++$issueid;	# Unique ID

  } elsif (/^ *agenda *[:：] *($urlpat) *$/i) {
    $agenda = '<a href="' . esc($1) . "\">$agenda_icon</a>\n";
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *agenda *[:：] *(.*?) *$/i) {
    push(@diagnostics, "Found 'Agenda:' not followed by a URL: '$1'.");
    # $records[$i]->{type} = 'o';	# Omit line from output

  } elsif (/^ *meeting *[:：] *(.*?) *$/i) {
    $meeting = esc($1);
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *previous +meeting *[:：] *($urlpat) *$/i) {
    $prev_meeting = '<a href="' . esc($1) . "\">$previous_icon</a>\n";
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *next +meeting *[:：] *($urlpat) *$/i) {
    $next_meeting = '<a href="' . esc($1) . "\">$next_icon</a>\n";
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *(previous|next) +meeting *[:：] *(.*?) *$/i) {
    push(@diagnostics,"Found '$1 meeting:' not followed by a URL: '$2'.");
    # $records[$i]->{type} = 'o';	# Omit line from output

  } elsif (/^ *chairs? *-[:：]? *$/i) {
    delete $chairs{fc $records[$i]->{speaker}}; # Remove speaker from chairs
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *chairs? *-[:：]? *(.*?) *$/i) {
    delete $chairs{fc $_} foreach (split(/ *, */, $1)); # Remove given chairs
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *chairs? *\+[:：]? *$/i) {
    my $s = $records[$i]->{speaker};
    $chairs{fc $s} = $s;		# Add to collected chairs
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *chairs? *[:：] *$/i) {
    push(@diagnostics, "Ignored empty command \"$records[$i]->{text}\"");

  } elsif (/^ *chairs? *([:：]|\+[:：]?) *(.*?) *$/i) {
    %chairs = () if $1 eq ':' || $1 eq '：'; # Reset the list of chairs
    $chairs{fc $_} = $_ foreach (split(/ *, */, $2)); # Add all to chairs list
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *date *[:：] *(\d+ \w+ \d+)/i) {
    $date = $1;
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *scribe(?:nick)? *-[:：]? *$/i) {
    delete_scribes($records[$i]->{speaker}, \%curscribes);
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *scribe(?:nick)? *\+[:：]? *$/i) {
    add_scribes($records[$i]->{speaker}, \%curscribes, \%scribes);
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *scribe(?:nick)? *[:：] *$/i) {
    push(@diagnostics, "Ignored empty command \"$records[$i]->{text}\"");

  } elsif (/^ *scribe(?:nick)? *([:：]|\+[:：]?) *($scribepat(?:, *$scribepat)*)$/i) {
    %curscribes = () if $1 eq ':' || $1 eq '：'; # Reset scribe nicks
    add_scribes($2, \%curscribes, \%scribes);
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *scribe *[:：] *([^ ].*?) *$/i) {
    # Probably an old-fashioned scribe command without a nick
    $scribes{fc $1} = $1;		# Add to collected scribe list
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif (/^ *scribe(?:nick)? *-[:：]? *([^ ].*)? *$/i) {
    delete_scribes($1, \%curscribes);
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif ($use_zakim && $records[$i]->{speaker} eq 'Zakim' &&
	   (/^agendum \d+\. "(.*)" taken up/ ||	   # Old Zakim
	    /^agendum \d+ -- (.*)/)) {		   # New Zakim
    $records[$i]->{type} = 't';		# Mark as topic line
    $records[$i]->{text} = $1;
    $records[$i]->{text} =~ s/ -- taken up \[from.*//;
    $records[$i]->{id} = ++$topicid;	# Unique ID

  } elsif ($use_zakim && $records[$i]->{speaker} eq 'Zakim' &&
	   /the attendees (?:were|have been) (.*?),?$/){
    $present{fc $_} = $_ foreach split(/, */, ($1 =~ s/\(no one\)//r));
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif ($use_zakim && $records[$i]->{speaker} eq 'Zakim' &&
	   /^\.\.\. (.*)$/) {
    my $s = $1;				# See what this is a continuation of
    my $j = $i - 1;
    $j-- while $j >= 0 && ($records[$j]->{text} =~ /^\.\.\. / ||
			   $records[$j]->{speaker} ne 'Zakim');
    if ($j >= 0 && $records[$j]->{text} =~ /the attendees (?:were|have been) /){
      $present{fc $_} = $_ foreach grep($_ ne '', split(/, */, $s));
    } elsif ($j >= 0 && $records[$j]->{text} =~ /, you wanted /) {
      $records[$j]->{text} .= ' ' . $s;
    } elsif ($j >= 0 && $records[$j]->{type} eq 't') { # Continued agendum
      $records[$j]->{text} .= ' ' . $s;
      $records[$j]->{text} =~ s/ -- taken up \[from.*//;
    }
    $records[$i]->{type} = 'o';		# Omit line from output

  } elsif ($use_zakim && $records[$i]->{speaker} eq 'Zakim' &&
	   /[^ ,]+, you wanted /) {
    # Leave Zakim's lines of the form: "Jim, you wanted to ..."

  } elsif ($use_zakim && $records[$i]->{speaker} eq 'Zakim') {
    $records[$i]->{type} = 'o';		# Ignore most conversations with Zakim

  } elsif ($use_zakim &&
    ( /^ *zakim,/i ||
      /^ *(?:chair +)?(?:ack|recognize)s? \w/i ||
      /^ *agg?enda *\d* *[\+\-\=\?]/i ||
      /^ *(?:delete|drop|forget|remove) +agend(?:um|a) +\d+ *$/i ||
      /^ *(?:take +up +|open +|move +to +)?(?:agend(?:um|a) +|next +agend(?:um|a))/i ||
      /^ *next +agend(?:um|a) *$/i ||
      /^ *(?:skip|(?:really +)?close) +(?:this +agend(?:um|a)|agend(?:um|a) +\d+) *$/i ||
      /^ *q(?:ueue|q)? *[-+=?]/i ||
      /^ *(?:ple?a?se? +)?(?:show +)?(?:the +)?(?:verbose +|full +)?q(?:ueue)?\?? *$/i ||
      /^ *(?:vqueue|vq|qv)\?/i ||
      /^ *[-+=?] *q(?:ueue|q)?\b/i ||
      /^ *(?:ple?a?se? +)?clear +(?:the +)?agenda *$/i ||
      /^ *(?:(?:list|show) +(?:all +)?(?:the +)?questions|questions *\?) *$/i ||
      /^ *(?:drop|close) +question +[0-9]+ *$/i)) {
    $records[$i]->{type} = 'o';		# Ignore most conversations with Zakim

  } elsif (/^ *trackbot *, *(?:(?:dis)?associate|bye|start|end|status)\b/i) {
    $records[$i]->{type} = 'o';		# Ignore some commands to trackbot

  } elsif ($records[$i]->{speaker} eq 'trackbot' &&
	   /^([a-zA-Z]+-[0-9]+) -- (.*)$/) {
    $records[$i]->{type} = 'B';		# A structured response from trackbot
    $records[$i]->{id} = $2;
    $records[$i]->{text} = $1;

  } elsif ($records[$i]->{speaker} eq 'trackbot' && /^$urlpat$/i) {
    my $j = $i - 1;			# A URL response from trackbot
    $j-- while $j >= 0 && ($records[$j]->{type} eq 'o' ||
			   $records[$j]->{speaker} ne 'trackbot');
    if ($j < 0) {			# URL belongs to nothing?
      $records[$i]->{type} = 'b';
    } else {				# Make previous line into a link
      $records[$j]->{text} = '->'.$records[$i]->{text}.' '.$records[$j]->{text};
      $records[$i]->{type} = 'o';
    }

  } elsif ($records[$i]->{speaker} eq 'trackbot') {
    $records[$i]->{type} = 'b'		# A response from trackbot

  } elsif ($records[$i]->{speaker} eq 'agendabot') {
    $records[$i]->{type} = 'o';		# Ignore most conversations w/ agendabot

  } elsif (/^ *agendabot *,/i) {
    $records[$i]->{type} = 'o';		# Ignore most conversations w/ agendabot

  } elsif (! $ghurlbot && /^ *ghurlbot *,/i) {
    $records[$i]->{type} = 'o';		# Ignore other commands to ghurlbot

  } elsif (! $ghurlbot && $records[$i]->{speaker} eq 'ghurlbot') {
    $records[$i]->{type} = 'o';		# Ignore if --noghurlbot was set

  } elsif ($records[$i]->{speaker} eq 'ghurlbot' &&
	   /^($urlpat) -> ((?:Issue |Action |Pull Request |\#)[0-9]+) ?(.*)$/i) {
    $records[$i]->{type} = 'B';		# A structured response from ghurlbot
    $records[$i]->{id} = $3;
    $records[$i]->{text} = "->$1 $2";

  } elsif ($records[$i]->{speaker} eq 'ghurlbot' &&
	   /^($urlpat) -> (@.*)$/i) {	# A link to a GitHub user
    $records[$i]->{type} = 'B';
    $records[$i]->{id} = '';
    $records[$i]->{text} = "->$1 $2";

  } elsif ($records[$i]->{speaker} eq 'ghurlbot' &&
	   /^(?:Cannot|Closed|Reopened|Created)/) {
    $records[$i]->{type} = 'b';

  } elsif ($records[$i]->{speaker} eq 'ghurlbot' && /^(?:[^ ,]+, )?OK\.?/) {
    $records[$i]->{type} = 'o';		# Ignore "OK" responses from ghurlbot

  } elsif (/^ *namedanchorhere *[:：] *(.*?) *$/i) {
    my $a = $1 =~ s/ /_/gr;
    if ($a =~ /^$/) {
      push(@diagnostics, "Empty named anchor ignored.");
    } elsif ($a =~ /^x[0-9][0-9]+$/) {
      push(@diagnostics, "Named anchor \"$a\" ignored. (\"xNN\" is reserved.)");
    } elsif ($a =~ /^(?:(?:Action|Resolution)Summary|links|attendees|toc|meeting)$/) {
      push(@diagnostics, "Named anchor \"$a\" ignored. (The name is reserved.)");
    } elsif (exists $namedanchors{$a}) {
      push(@diagnostics, "Duplicate named anchor \"$a\" ignored.");
    } else {
      $records[$i]->{type} = 'n';
      $records[$i]->{id} = esc($a);
      $namedanchors{$a} = 1;
    }

  } elsif ($is_scribe && /^ *\Q<$records[$i]->{speaker}\E>/i) {
    # Ralph's escape for a scribe's personal remarks: "<mynick> my opinion"
    $records[$i]->{text} =~ s/^.*?> ?//i;

  } elsif ($is_scribe && /^ *\\(.*)/) {			# Starts with backslash
    $records[$i]->{type} = 'd';				# Descriptive text
    $records[$i]->{text} = $1;				# Remove backslash

  } elsif (/^ *\\(.*)/) {				# Starts with backslash
    $records[$i]->{text} = $1;				# Remove backslash

  } elsif ($is_scribe &&
	   (/^($speakerpat) *[:：] *(.*)$/ ||
	    (!$spacecont && /^ +($speakerpat) *[:：] *(.*)$/)) &&
	   $records[$i]->{type} ne 'c' &&	# ... and not a failed s///
	   ! /^ *$urlpat/i &&			# ... and not a URL
	   ! /^ *$specialpat *[:：]/i) {	# ... nor special
    # A speaker line
    $records[$i]->{type} = 's';		# Mark as scribe line
    $lastspeaker{$records[$i]->{speaker}} = $1; # For any continuation lines
    $records[$i]->{speaker} = $1;
    $records[$i]->{text} = $2;
    $speakers{fc $1} = ++$speakerid if !exists $speakers{fc $1};

  } elsif ($is_scribe && defined $lastspeaker{$records[$i]->{speaker}} &&
	   (/^ *(?:\.\.\.*|…) *(.*?) *$/ ||
	    ($implicitcont && /^ *(.*?) *$/) ||
	    ($spacecont && /^ +(.*?) *$/)) &&
	   $records[$i]->{type} ne 'c') { # ... and not a failed s///
    # Looks like a continuation line
    $records[$i]->{speaker} = $lastspeaker{$records[$i]->{speaker}};
    $records[$i]->{type} = 's';		# Mark as scribe line
    my $j = $i - 1; $j-- while $j > 0 && $records[$j]->{type} eq 'o';
    if ($j >= 0 && $records[$j]->{type} eq 's' &&
	$records[$j]->{speaker} eq $records[$i]->{speaker}) {
      # Concatenate previous and current line and remove previous line
      $records[$i]->{text} = $records[$j]->{text} . "\t" . $1;
      $records[$j]->{type} = 'o';	# Omit previous line from output
    } else {
      # Cannot concatenate with previous line, remove "..." instead.
      $records[$i]->{text} = $1;
    }

  } elsif (/^ *(?:\.\.\.*|…) *(.*?) *$/) {
    # Is this a continuation of an action/resolution/issue/topic?
    my ($s, $j, $speaker) = ($1, $i - 1, $records[$i]->{speaker});
    $j-- while $j > 0 && ($records[$j]->{type} eq 'o' ||
			  $records[$j]->{speaker} ne $speaker);
    if ($j >= 0 && $records[$j]->{type} =~ /[artTuUd]/) {
      $records[$j]->{text} .= "\t" . $s;
      $records[$i]->{type} = 'o';	# Omit this line from output
    } elsif ($is_scribe) {
      # Not a continuation of anything, but it is by the scribe.
      $records[$i]->{type} = 'd';		# Mark as descriptive text
      $lastspeaker{$speaker} = undef;		# No continuation expected
    }

  } elsif ($is_scribe && $records[$i]->{type} eq 'c') {
    # It's a failed s/// command by the speaker. Leave it as a 'c'.

  } elsif ($is_scribe && /^ *-> *$urlpat/i) {
    # If the scribe used a Ralph-link (-> url ...), still allow continuations
    $records[$i]->{type} = 'd';		# Mark as descriptive text

  } elsif ($is_scribe) {
    $records[$i]->{type} = 'd';		# Mark as descriptive text
    $lastspeaker{$records[$i]->{speaker}} = undef; # No continuation expected
  }
}

# If date wasn't given, guess it from a URL, if any
if (!defined $date && defined $minutes_url &&
    $minutes_url =~ m|/(\d\d\d\d)/(\d\d)/(\d\d)-|) {
  $date = $3 . ' ' . $month[0+$2] . ' ' . $1;
} elsif (!defined $date && defined $logging_url &&
	 $logging_url =~ m|/(\d\d\d\d)/(\d\d)/(\d\d)-|) {
  $date = $3 . ' ' . $month[0+$2] . ' ' . $1;
} elsif (!defined $date) {
  $date = "";
  push(@diagnostics, "Found no dated URLs. You may need to use 'Date:'.");
}

# Add lists of (1) speakers that do not appear in %present; (2) all
# speakers; and (3) all people active on IRC.
#
my @all_speakers = fc_uniq(map $_->{speaker}, grep $_->{type} eq 's', @records);
my @also = grep !exists($present{fc $_}), @all_speakers;
push @diagnostics, "Maybe present: " .
    join(", ", sort {fc($a) cmp fc($b)} @also) if @also;
push @diagnostics, "All speakers: " .
    join(", ", sort {fc($a) cmp fc($b)} @all_speakers) if @all_speakers;
push @diagnostics, "Active on IRC: " .
    join(", ", sort {fc($a) cmp fc($b)} keys %count) if %count;

# Step 6. Convert records to HTML and then fill a template.
#
# Each type of record is converted to a specific HTML fragment, with
# %1$s replaced by the speaker, %2$s by the ID, %3$s by the text, %4$s
# by the speaker ID, %5$s by a unique ID for the record and %6$s by a
# link to a recording of the meeting, if any.
#
# The 1 or 0 after the pattern indicates whether the text (%3$) can be
# parsed for emphasis and math. (Only applicable if --emphasis was
# specified.)
#
# Also replace \t (i.e., placeholders for line breaks) as appropriate.
#
my $embedded_recording = $recording;
my $canonical_recording = $recording;
if (defined $recording) {
  # Modify URL for certain known video sites.
  if ($recording =~ /^https:\/\/youtu\.be\/(.*)$/) {
    $canonical_recording = "https://www.youtube.com/watch?v=" . $1;
  }
  if ($canonical_recording =~ /youtube\.com\/watch\?v=/) {
    $embedded_recording = $canonical_recording =~ s/watch\?v=/embed\//r;
    $embedded_recording .= "?enablejsapi=1&amp;rel=0&amp;modestbranding=1";
  } elsif ($canonical_recording =~ /watch\.videodelivery\.net\//) {
    $embedded_recording = $canonical_recording =~ s/watch\./iframe\./r;
  }
}

my %linepat = (
  a => ["<p id=%2\$s class=action><strong>ACTION:</strong> %3\$s</p>\n", 1],
  b => ["<p id=%5\$s class=bot><cite>&lt;%1\$s&gt;</cite> %3\$s</p>\n", 0],
  B => ["<p id=%5\$s class=bot><cite>&lt;%1\$s&gt;</cite> <strong>%3\$s</strong> %2\$s</p>\n", 0],
  d => ["<p id=%5\$s class=summary>%3\$s</p>\n", 1],
  D => ["<pre id=%5\$s class=summary>\n%3\$s</pre>\n", 0],
  i => [$scribeonly ? '' : "<p id=%5\$s class=irc><cite>&lt;%1\$s&gt;</cite> %3\$s</p>\n", 1],
  I => [$scribeonly ? '' : "<p id=%5\$s class=irc><cite>&lt;%1\$s&gt;</cite> <code>%3\$s</code></p>\n", 0],
  c => [$scribeonly ? '' : "<p id=%5\$s class=irc><cite>&lt;%1\$s&gt;</cite> %3\$s</p>\n", 0],
  o => ['', 0],
  r => ["<p id=%2\$s class=resolution><strong>RESOLUTION:</strong> %3\$s</p>\n",, 1],
  s => ["<p id=%5\$s class=\"phone %4\$s\"><cite>%1\$s:</cite> %3\$s</p>\n", 1],
  n => ["<p class=anchor id=\"%2\$s\"><a href=\"#%2\$s\">⚓</a></p>\n", 0],
  u => ["<p id=%2\$s class=issue><strong>ISSUE:</strong> %3\$s</p>\n", 1],
  T => ["<h4 id=%2\$s>%3\$s%6\$s</h4>\n", 1],
  t => ["</section>\n\n<section>\n<h3 id=%2\$s>%3\$s%6\$s</h3>\n", 1],
  slideset => ["<p id=%5\$s class=summary>Slideset: %3\$s</p>\n", 0],
  slide => ["<p id=%5\$s class=summary><a class=islide href=\"%2\$s\">[Slide %3\$s]</a></p>\n", 1],
  repo => ["<p id=%5\$s class=summary>Repository: %3\$s</p>\n", 0],
  drop => ["<p id=%5\$s class=summary>Repository- %3\$s</p>\n", 1],
    );

my $minutes = '';
foreach my $p (@records) {
  if ($github) {
    if ($p->{type} eq 'repo' && $p->{text} eq '') {
      # An empty repo line resets the list of repositories.
      @repositories = ();
    } elsif ($p->{type} eq 'repo') {
      # A repo line adds repositories to use for issues in the next lines.
      add_repositories($p->{text});
    } elsif ($p->{type} eq 't' || $p->{type} eq 'T') {
      # GitHub repositories in topic lines are added to the repositories.
      add_repositories($1) while $p->{text} =~ /($githuburl)/g;
    } elsif ($p->{type} eq 'drop') {
      # Remove the given repository.
      remove_repositories($p->{text});
    }
  }
  # The last part generates nothing, but avoids warnings for unused args.
  my $line = sprintf $linepat{$p->{type}}[0] . '%1$.0s%2$.0s%3$.0s%4$.0s%5$.0s%6$.0s',
      esc($p->{speaker}),						    # %1
      $p->{id} // '',							    # %2
      esc($p->{text}, $emphasis && $linepat{$p->{type}}[1], 1, 1, $github), # %3
      $speakers{fc $p->{speaker}} // '',				    # %4
      ++$lineid,							    # %5
      link_to_recording($canonical_recording, $p->{time});		    # %6
  if (!$keeplines) {
    $line =~ tr/\t/ /;
  } elsif ($line =~ /\t/) {
    $line =~ s|\t|"<br>\n<span id=" . ++$lineid . ">… "|e; # First line
    $line =~ s|\t|"</span><br>\n<span id=" . ++$lineid . ">… "|ge; # Others
    $line =~ s|</p>|</span></p>|; # Last line
  }
  $minutes .= $line;
}

# @stylesheets is an array of triples [alt, title, url], where alt = 0
# means this is the default style, not 0 means an "alternate" style.
#
my $alt = 0;
my $w3 = 'https://www.w3.org';
my @stylesheets = ();
push @stylesheets, [$alt++, "Default", $stylesheet] if defined $stylesheet;
if ($styleset eq 'team') {
  push @stylesheets,
      [$alt + $old_style, "2018", "$w3/StyleSheets/scribe2/team.css"],
      [$alt + !$old_style, "2004", "$w3/StyleSheets/base.css"],
      [$alt + !$old_style, "2004", "$w3/StyleSheets/team.css"],
      [$alt + !$old_style, "2004", "$w3/StyleSheets/team-minutes.css"],
      [$alt + !$old_style, "2004", "$w3/2004/02/minutes-style.css"],
      [1, "Typewriter", "$w3/StyleSheets/scribe2/tt-team.css"];
} elsif ($styleset eq 'member') {
  push @stylesheets,
      [$alt + $old_style, "2018", "$w3/StyleSheets/scribe2/member.css"],
      [$alt + !$old_style, "2004", "$w3/StyleSheets/base.css"],
      [$alt + !$old_style, "2004", "$w3/StyleSheets/member.css"],
      [$alt + !$old_style, "2004", "$w3/StyleSheets/member-minutes.css"],
      [$alt + !$old_style, "2004", "$w3/2004/02/minutes-style.css"],
      [1, "Typewriter", "$w3/StyleSheets/scribe2/tt-member.css"];
} else {			# 'public' or 'fancy'
  my $f = $styleset eq 'fancy';
  push @stylesheets,
      [$alt + $old_style + $f, "2018", "$w3/StyleSheets/scribe2/public.css"],
      [$alt + !$old_style + $f, "2004", "$w3/StyleSheets/base.css"],
      [$alt + !$old_style + $f, "2004", "$w3/StyleSheets/public.css"],
      [$alt + !$old_style + $f, "2004", "$w3/2004/02/minutes-style.css"],
      [$alt + !$f, "Fancy", "$w3/StyleSheets/scribe2/fancy.css"],
      [1, "Typewriter", "$w3/StyleSheets/scribe2/tt-member.css"];
}

# Format some of the variables used in the template below
#
my $style = join("\n",
  map {"<link rel=\"" . ($_->[0] ? "alternate " : "") . "stylesheet\" " .
    "type=\"text/css\" title=\"$_->[1]\" href=\"$_->[2]\">"} @stylesheets);

my $scripts = '';
$scripts .= "<script src=\"$mathjax\" id=MathJax-script async></script>\n"
    if $emphasis && $has_math;
$scripts .= "<script type=module src=\"$islide\"></script>\n"
    if $has_slides;

if (defined $recording) {
  $scripts .= "<script src=\"https://www.youtube.com/iframe_api\"></script>\n"
      if $canonical_recording =~ /^https:\/\/(www\.)?youtube\.com\//;
  # Copy the script whose code is further down between __DATA__ and __END__:
  $scripts .= $_ while ($_ = <main::DATA>) !~ /^__END__/;
}
close main::DATA;

$logo = "<p>$logo</p>\n\n" if defined $logo && $logo ne '';
$logo = '' if !defined $logo && ($styleset eq 'fancy');
$logo = "<p>$w3clogo</p>\n\n" if !defined $logo;
my $draft = $final ? "" : "&ndash; DRAFT &ndash;<br>\n";
my $log = defined $logging_url?"<a href=\"$logging_url\">$irclog_icon</a>\n":"";
my $present = esc(join(", ", map($present{$_}, sort keys %present))) || '-';
$present = "<details><summary>".($present =~ s/,/,<\/summary>/r)."</details>"
  if scalar keys %present > $collapse_limit; # Collapsed if the list is long
my $regrets = esc(join(", ", map($regrets{$_}, sort keys %regrets))) || '-';
$regrets = "<details><summary>".($regrets =~ s/,/,<\/summary>/r)."</details>"
  if scalar keys %regrets > $collapse_limit; # Collapsed if the list is long
my $scribes = esc(join(", ", sort {fc($a) cmp fc($b)} values %scribes)) || '-';
my $chairs = esc(join(", ", sort {fc($a) cmp fc($b)} values %chairs)) || '-';
my $diagnostics = !$embed_diagnostics || !@diagnostics ? "" :
  "<div class=diagnostics>\n<h2>Diagnostics<\/h2>\n" .
  join("", map {"<p class=warning>" . esc($_) . "</p>\n"} @diagnostics) .
  "</div>\n";
my $videoplayer = ! defined $recording ? '' :
    "<section id=recording>\n" .
    "<p class=summary>Recording: $recording_link\n" .
    "<div class=video>\n" .
    "<iframe src=\"$embedded_recording\" " .
    "width=600 height=340 type=\"text/html\" frameborder=0 allowfullscreen " .
    "allow=\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\"></iframe>\n" .
    "</div>\n" .
    "</section>\n";

# Collect lists of actions, resolutions and issues from the @records.
# Wrap each list in a <div> and add a corresponding item in the ToC
# (unless the list is empty).
#
my $actions = join("",
		   map("<li><a href=\"#" . $_->{id} . "\">" .
		       esc($_->{text}, $emphasis, -1, 1) . "</a></li>\n",
		       grep($_->{type} eq 'a', @records)));
my $actiontoc = !$actions ? '' :
    "<li class=app><a href=\"#ActionSummary\">Summary of action items</a></li>\n";
$actions = "\n<div id=ActionSummary>\n<h2>Summary of action items</h2>
<ol>\n$actions</ol>\n</div>\n" if $actions;
if ($keeplines) {$actions =~ s/\t/<br>\n… /g;} else {$actions =~ tr/\t/ /;}

my $resolutions = join("",
		       map("<li><a href=\"#" . $_->{id} . "\">" .
			   esc($_->{text}, $emphasis, -1, 1) . "</a></li>\n",
			   grep($_->{type} eq 'r', @records)));
my $resolutiontoc = !$resolutions ? '' :
    "<li class=app><a href=\"#ResolutionSummary\">Summary of resolutions</a></li>\n";
$resolutions = "\n<div id=ResolutionSummary>\n<h2>Summary of resolutions</h2>
<ol>\n$resolutions</ol>\n</div>\n" if $resolutions;
if ($keeplines) {$resolutions =~ s/\t/<br>\n… /g;} else {$resolutions =~ tr/\t/ /;}

my $issues = join("",
		  map("<li><a href=\"#" . $_->{id} . "\">" .
		      esc($_->{text}, $emphasis, -1, 1) . "</a></li>\n",
		      grep($_->{type} eq 'u', @records)));
my $issuetoc = !$issues ? '' :
    "<li class=app><a href=\"#IssueSummary\">Summary of issues</a></li>\n";
$issues = "\n<div id=IssueSummary>\n<h2>Summary of issues</h2>
<ol>\n$issues</ol>\n</div>\n" if $issues;
if ($keeplines) {$issues =~ s/\t/<br>\n… /g;} else {$issues =~ tr/\t/ /;}

# Collect topics (records with type 't' or 'T') for the ToC.
#
my $topics = '';
my $prev_level = ' ';
foreach my $t (grep($_->{type} =~ /^[Tt]$/, @records)) {
  my $s = "<li><a href=\"#" . $t->{id} . "\">" .
      esc($t->{text}, $emphasis, -1, 1) . "</a>";
  if ($prev_level eq $t->{type}) {$topics .= "</li>\n$s"}
  elsif ($prev_level eq 't') {$topics .= "\n<ol>\n$s"}
  elsif ($prev_level eq 'T') {$topics .= "</li>\n</ol>\n</li>\n$s"}
  elsif ($t->{type} eq 't') {$topics .= $s}
  else {$topics .= "<li>\n<ol>\n$s"}
  $prev_level = $t->{type};
}
if ($prev_level eq 'T') {$topics .= "</li>\n</ol>\n</li>\n"}
elsif ($prev_level eq 't') {$topics .= "</li>\n"}
if ($keeplines) {$topics =~ s/\t/<br>\n… /g;} else {$topics =~ tr/\t/ /;}

# And output the formatted HTML.
#
print "<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=utf-8>
<title>$meeting &ndash; $date</title>
<meta name=viewport content=\"width=device-width\">
$style
$scripts</head>

<body>
<header>
$logo<h1>$draft$meeting</h1>
<h2>$date</h2>

<nav id=links>
$prev_meeting$agenda$log$next_meeting</nav>
</header>

<div id=prelims>
<div id=attendees>
<h2>Attendees</h2>
<dl class=intro>
<dt>Present</dt><dd>$present</dd>
<dt>Regrets</dt><dd>$regrets</dd>
<dt>Chair</dt><dd>$chairs</dd>
<dt>Scribe</dt><dd>$scribes</dd>
</dl>
</div>

<nav id=toc>
<h2>Contents</h2>
<ol>
$topics$actiontoc$resolutiontoc$issuetoc</ol>
</nav>
</div>

<main id=meeting class=meeting>
<h2>Meeting minutes</h2>
$videoplayer<section>$minutes</section>
</main>
$actions$resolutions$issues

<address>Minutes manually created (not a transcript), formatted by <a
href=\"https://w3c.github.io/scribe2/scribedoc.html\"
>scribe.perl</a> version $revision ($versiondate).</address>

$diagnostics</body>
</html>
";

print STDERR map("* $_\n", @diagnostics) if !$embed_diagnostics;


# The Javascript code that adds play/pause buttons when generated
# minutes with an embedded video are displayed in a browser.
# The code ends at __END__.

__DATA__
<script type=module>
const recordingUrl = document.querySelector("#recording a")?.href;
const embed = document.querySelector("#recording iframe");
let playing = false;

// monitoring player state
if (embed) {
  if (embed.src.match(/^https:\/\/(www\.)?youtube\.com\//)) {
    window.onYouTubeIframeAPIReady = () => {
      embed.id = "player";
      window.player = new YT.Player(embed.id);
      window.player.addEventListener("onStateChange", e => {
        if (e.data === YT.PlayerState.PLAYING)
          playing = true;
        else if (e.data === YT.PlayerState.PAUSED || e.data === YT.PlayerState.ENDED)
          playing = false;
      });
    };
  } else {
    window.addEventListener("message", e => {
      if (e.data[0] === "play") playing = true;
      else if (e.data[0] === "pause" || e.data[0] === "ended") playing = false;
    });
  }
}

function sendVideoCommand(command, args)
{
  let msg;
  if (embed.src.match(/^https:\/\/(www\.)?youtube\.com\//)) {
    const commands = {'play': 'playVideo', 'pause': 'pauseVideo', 'seek': 'seekTo'};
    msg = JSON.stringify({
      event: 'command',
      func: commands[command],
      args
    });
  } else {
    msg = [command, ...args];
  }
  embed.contentWindow.postMessage(msg, '*');
}

function showVideoIfNeeded()
{
  const windowScrollTop = window.pageYOffset;
  const {top} = embed.getBoundingClientRect();
  const videoBottom = parseInt(embed.height, 10) + top;
  if (windowScrollTop > videoBottom && playing)
    embed.parentNode.classList.add('stuck');
  else
    embed.parentNode.classList.remove('stuck');
}

function videoPlayHandler(e)
{
  if (!embed) return;
  const el = e.target;
  const offset = parseInt(el.dataset.offset, 10);
  if (offset && !isNaN(offset) && !el.dataset.lastHit)
    sendVideoCommand('seek', [offset]);
  sendVideoCommand('play');
  playing = true;
  showVideoIfNeeded();
  document.querySelectorAll("button.playBtn").forEach(
    el => delete el.dataset.lastHit);
  el.dataset.lastHit = true;	// So we know when the same button is hit twice
}

function videoPauseHandler(e)
{
  if (!embed) return;
  sendVideoCommand('pause');
  playing = false;
}

// Add play & pause buttons
if (recordingUrl) {
  document.querySelectorAll("a.recording[href]").forEach(el => {
    const playBtn = document.createElement("button");
    playBtn.className = "play";
    playBtn.dataset.offset = new URL(el.href).hash.split("=")[1];
    el.insertAdjacentElement("afterend", playBtn);
    playBtn.addEventListener("click", videoPlayHandler);
    playBtn.title = "Play embedded recording from this point of the meeting";
    playBtn.textContent = "▶";

    const pauseBtn = document.createElement("button");
    playBtn.insertAdjacentElement("afterend", pauseBtn);
    pauseBtn.className = "pause";
    pauseBtn.addEventListener("click", videoPauseHandler);
    pauseBtn.title = "Pause recording";
    pauseBtn.textContent = "⏸\uFE0E";
  });

  window.addEventListener("scroll", showVideoIfNeeded, {passive: true});
}
</script>
__END__

=head1 NAME

scribe.perl - Turn an IRC log of a meeting into minutes in HTML

=head1 SYNOPSIS

scribe.perl [options] [file ...]

  --help		Brief help message
  --team		Use team style
  --member		Use member style
  --fancy		Use fancy style
  --embedDiagnostics	Put diagnostics in the minutes instead of on stderr
  --implicitContinuations	Continuation lines do not need `...'
  --allowSpaceContinuation	Allow initial space as well as `...'
  --keepLines		Do not rewrap lines (default)
  --urlDisplay=break	Allow URLs to break at slashes (default)
  --urlDisplay=shorten	Shorten URLs by omitting the middle part
  --urlDisplay=full	Do not shorten or break URLs
  --final		Omit the word `DRAFT' from the minutes
  --draft		Include the word `DRAFT' in the minutes (default)
  --scribenick		Initial list of scribe nicks, comma-separated
  --dashTopics		Allow a line of dashes to start a new topic
  --useZakimTopics	Parse Zakim's lines for agenda topics (default)
  --scribeOnly		Omit all text that is not written by a scribe
  --emphasis		Allow smileys, arrows and inline styles
  --mathjax=URL		Use a specific MathJax (only with --emphasis)
  --islide=URL		Use a specific i-slide library
  --oldStyle		Use the style of scribe.perl version 1
  --minutes=URL		Used to guess a date if the URL contains YYYY/MM/DD
  --logo=markup		Replace the W3C link and logo with this HTML markup
  --nologo      	Same as --logo=""
  --nogithubIssues	Do not make GitHub issue numbers into links
  --noghurlbot		Omit messages from GHURLBot
  --stylesheet=URL	Use this style sheet instead of the default
  --collapseLimit=n     Collapse the participant list if there are more (30)

You can use single dash (-) or double (--). Options are
case-insensitive and can be abbreviated. Some options can be negated
with `no' (e.g., --nokeeplines). For the full manual see
L<https://w3c.github.io/scribe2/scribedoc.html>
scribedoc.html>
