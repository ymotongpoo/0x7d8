//
//  NanitabeAppDelegate.m
//  Nanitabe
//
//  Created by daisuke on 09/04/29.
//  Copyright __MyCompanyName__ 2009. All rights reserved.
//

#import "NanitabeAppDelegate.h"
#import "RootViewController.h"


@implementation NanitabeAppDelegate

@synthesize window;
@synthesize navigationController;
@synthesize list;


- (void)applicationDidFinishLaunching:(UIApplication *)application {
	list = [[NSMutableArray alloc] initWithObjects:@"炊き込みご飯", @"その他", @"その他", @"その他", @"その他", @"その他", nil];
	
	// Configure and show the window
	[window addSubview:[navigationController view]];
	[window makeKeyAndVisible];
}


- (void)applicationWillTerminate:(UIApplication *)application {
	// Save data if appropriate
}


- (void)dealloc {
	[navigationController release];
	[window release];
	[super dealloc];
}

@end
